import subprocess
import re

def make_sort_ciffile(dir):
    cifdir_ = subprocess.getoutput("find {0} -type d | sort".format(dir))
    cifdir = cifdir_.split('\n')
    del cifdir[0]
    isiteinfo=list()
    for i in cifdir:
        cifid=re.split('/',i)[-1]
        lasttxt=subprocess.getoutput("grep ' Si' {}/{}.txt |tail -n 1".format(i,cifid))
        try:
            maxisite=int(re.split('Si',lasttxt)[0].replace(' ',''))
        except:
            continue
        isiteinfo.append((i,maxisite))
    isiteinfo.sort(key=lambda x:x[1])

    estimecont=2000
    cont=0
    picupadress=list()
    for i in isiteinfo:
        cont+=i[1]
        picupadress.append(i)
        if cont>=estimecont:
            break
        continue
    print(cont)
    import pandas as pd
    info=pd.DataFrame(picupadress,columns=['cifadress','Si_len'])
    info.to_csv('{}/picupadress'.format(dir))
