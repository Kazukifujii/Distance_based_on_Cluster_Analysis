import pandas as pd
import subprocess
import time
import os
import shutil
outdirpaths = 'zeolitecifs'

#zeoliteのcifファイルをダウンロードする
download_base_address = lambda cifid:f'https://asia.iza-structure.org/IZA-SC/cif/{cifid}.cif'
table = pd.read_html('https://europe.iza-structure.org/IZA-SC/ftc_table.php')[1]

idlist = table.to_numpy().flatten().tolist()

#idlistの要素すべてを大文字のアルファベット3文字になるようにする
idlist = [cifid if len(cifid)==3 else cifid[1:] for cifid in idlist if isinstance(cifid,str)]

#出力先のディレクトリを作成
cwd = os.getcwd()
try:
    if os.path.exists(outdirpaths):
        shutil.rmtree(outdirpaths)
    os.mkdir(outdirpaths)
    os.chdir(outdirpaths)
    #ダウンロード
    for cifid in idlist:
        time.sleep(0.5)
        subprocess.run(f'wget {download_base_address(cifid)}',shell=True)
except Exception as e:
    print(f"Error : {str(e)}")
    raise e
finally:
    os.chdir(cwd)