import copy,os,glob,re
from operator import index
import sys
import pandas as pd
import subprocess
from collections import defaultdict

def make_fcluster_list(csvlist):
    if type(csvlist) is str:
        cifdirs=pd.read_csv(csvlist,index_col=0).cifadress.to_list()
    else:
        cifdirs= subprocess.getoutput("find {0} -type d | sort".format(csvlist))
        cifdirs= cifdirs.split('\n')
        del cifdirs[0]
    picinfo=list()
    cwd=os.getcwd()
    for _,cifdir in enumerate(cifdirs):
        cifid=re.split('/',cifdir)[-1]
        print(cifid)
        os.chdir(cifdir)
        try:
            csvn=glob.glob('*fcluster*')[0]
        except:
            print('no such file')
            continue
        info=pd.read_csv(csvn,index_col=0)
        picisite=copy.deepcopy(info.iloc[info.fclusternum.drop_duplicates().index].isite.values)
        picinfo_=[(cifid,cifdir,isite) for isite in picisite]
        picinfo+=picinfo_
        os.chdir(cwd)

    totalinfo=pd.DataFrame(picinfo,columns=['cifid','adress','isite'])
    totalinfo.to_csv('{}/allcif_cluster'.format(csvlist))

def make_isite_list(dir):
    #for i,adress in enumerate(csvlist):
    cifid=re.split('/',dir)[-1]
    ciflist=glob.glob('{}/{}_[0-9]*.csv'.format(dir,cifid))
    isitelist=[re.findall('[0-9]{1,}',csvname)[0] for csvname in ciflist]
    isitelist=list(set(isitelist))
    isitelist=[int(isitelist_) for isitelist_ in isitelist]
    isitelist.sort()
    picinfo=[(('{}').format(cifid),dir,isite) for isite in isitelist]
    resultdf=pd.DataFrame(picinfo,columns=['cifid','adress','isite'])
    resultdf.to_csv('{}/isite_list'.format(dir))
    return resultdf

from read_info import read_nood

def make_classification_ring(csvlist,outdir=None):
    if type(csvlist) is str:
        csvlist=pd.read_csv(csvlist,index_col=0)
    class_dict=defaultdict(list)
    
    for _,csv_ in csvlist.iterrows():
        csvname='{}/{}_{}_0.csv'.format(csv_.adress,csv_.cifid,csv_.isite)
        df=pd.read_csv(csvname,index_col=0).round(6)
        #counting duplicate isite
        disite=df.index.size-df.loc[:,'x':'z'].drop_duplicates().index.size
        nooddf=pd.DataFrame(read_nood(df)).astype(str)
        dnood=nooddf.index.size-nooddf.drop_duplicates().index.size
        ring=disite-dnood
        class_dict[str(ring)].append((csv_.cifid,csv_.adress,csv_.isite))
    
    for key,adress in class_dict.items():
        if not type(outdir) is str:
            pd.DataFrame(adress,columns=['cifid','adress','isite']).to_csv('cluster_adress_ring={}'.format(key))
        else:
            pd.DataFrame(adress,columns=['cifid','adress','isite']).to_csv('{}/cluster_adress_ring={}'.format(outdir,key))
