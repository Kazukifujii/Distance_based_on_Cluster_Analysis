from cmath import nan
from copy import deepcopy
import sys
import pandas as pd
import os,itertools,time,pulp
from joblib import Parallel,delayed

def calcost(data1,data2):
    data1c=data1.loc['x':'z']
    data2c=data2.loc['x':'z']
    redata=data1c-data2c
    if data1.atom==data2.atom:
        return redata.x**2+redata.y**2+redata.z**2
    return 1000

def cal_distance_df(clusterdf1,clusterdf2,values=False):
    cluster1=deepcopy(clusterdf1)
    cluster2=deepcopy(clusterdf2)
        #make cost and constrains
    costs=dict()
    for i,data1 in cluster1.iterrows():
        for j,data2 in cluster2.iterrows():
            cost=calcost(data1,data2)
            costs[(i,j)]=cost
    
    model=pulp.LpProblem('cluster_matching',pulp.LpMinimize)
    f=dict()
    obfunc=list()
    for index,cost in costs.items():
        i,j=index
        f[i,j]=pulp.LpVariable('index{}_{}'.format(i,j),lowBound=0)
        obfunc.append(f[i,j]*cost)
    model+=pulp.lpSum(obfunc)

    for i,data1 in cluster1.iterrows():
        model += pulp.lpSum([f[(i,j)] for j,_ in cluster2.iterrows()])==1

    for j,data2 in cluster2.iterrows():
        model+= pulp.lpSum([f[(i,j)] for i,_ in cluster1.iterrows()])==1

    result=model.solve(pulp.PULP_CBC_CMD(msg = False))
    
    if result==1:
        if values:
            val=list()
            for var_ in f.values():
                if var_.varValue!=0:
                    val.append((str(var_),float(var_.varValue)))
            return val
        dis_=float()
        sumf=float()
        for val in f.values():
            sumf+=val.varValue
        for key,val in f.items():
            dis_+=val.varValue*costs[key]
        return dis_/sumf
    else:
        return nan


def cal_distance(csv_adress1,csv_adress2,values=False):
    cluster1=pd.read_csv(csv_adress1,index_col=0)
    cluster2=pd.read_csv(csv_adress2,index_col=0)
    #make cost and constrains
    costs=dict()
    for i,data1 in cluster1.iterrows():
        for j,data2 in cluster2.iterrows():
            cost=calcost(data1,data2)
            costs[(i,j)]=cost
    
    model=pulp.LpProblem('cluster_matching',pulp.LpMinimize)
    f=dict()
    obfunc=list()
    for index,cost in costs.items():
        i,j=index
        f[i,j]=pulp.LpVariable('index{}_{}'.format(i,j),lowBound=0)
        obfunc.append(f[i,j]*cost)
    model+=pulp.lpSum(obfunc)

    for i,data1 in cluster1.iterrows():
        model += pulp.lpSum([f[(i,j)] for j,_ in cluster2.iterrows()])==1

    for j,data2 in cluster2.iterrows():
        model+= pulp.lpSum([f[(i,j)] for i,_ in cluster1.iterrows()])==1

    result=model.solve(pulp.PULP_CBC_CMD(msg = False))
    
    if result==1:
        if values:
            val=list()
            for var_ in f.values():
                if var_.varValue!=0:
                    val.append((str(var_),float(var_.varValue)))
            return val
        dis_=float()
        sumf=float()
        for val in f.values():
            sumf+=val.varValue
        for key,val in f.items():
            dis_+=val.varValue*costs[key]
        return dis_/sumf
    else:
        return nan

def parallel_self_distance(clusterdf,comb,pattern_j):
    index_i,index_j=comb
    data_i=clusterdf.loc[index_i]
    data_j=clusterdf.loc[index_j]
    csvi='{}/{}_{}_0.csv'.format(data_i.adress,data_i.cifid,data_i.isite,0)
    csvj='{}/{}_{}_{}.csv'.format(data_j.adress,data_j.cifid,data_j.isite,pattern_j)
    if not (os.path.isfile(csvi) and os.path.isfile(csvj)):
        return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,nan)
    disij=cal_distance(csvi,csvj)
    return ('{}_{}'.format(data_i.cifid,str(data_i.isite)),'{}_{}'.format(data_j.cifid,str(data_j.isite)),0,pattern_j,disij)

def make_distance_csv(listadress,resultname,outdir=False):
    tstime=time.perf_counter()
    if type(listadress) is str:
        all_cluster=pd.read_csv(listadress,index_col=0)
    elif type(listadress) is pd.DataFrame:
        all_cluster=listadress
    else:
        print('make_distance_csv error')
    all_index=all_cluster.index.to_list()
    comb=list(itertools.combinations(all_index,2))
    plist=[i for i in range(12)]
    alllen=12
    cont=0
    distance=list()
    for pi in plist:
        cont+=1
        print("\r"+str(cont)+'/'+str(alllen),end="")
        fstime=time.perf_counter()
        distance_=Parallel(n_jobs=-1)(delayed(parallel_self_distance)(all_cluster,comb_,pi) for comb_ in comb)
        distance+=distance_
        etiem=time.perf_counter()
        print('\ncomputation time {}'.format(etiem-fstime))
    disfile_colname=['isite_i','isite_j','pattern_i','pattern_j','distance']
    distancedf=pd.DataFrame(distance,columns=disfile_colname)
    if outdir:
        distancedf.to_csv('{}/{}'.format(outdir,resultname))
    else:
        distancedf.to_csv('{}'.format(resultname))
    print()
    print('output {}'.format(resultname))
    print('total computation time {}'.format(etiem-tstime))

