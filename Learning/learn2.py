import re
import csv

content='''10.170.109.202: E11587835LSLDXIANWUJU> st cell
10.170.109.202: 
10.170.109.202: 201109-11:14:37 10.170.109.202 20.0c MSRBS_NODE_MODEL_20.Q2_453.28212.68_480e stopfile=/tmp/41993
10.170.109.202: ===================================================================================
10.170.109.202: Proxy  Adm State     Op. State     MO
10.170.109.202: ===================================================================================
10.170.109.202:   854  1 (UNLOCKED)  1 (ENABLED)   GNBDUFunction=1,NRCellDU=E11587835LSLDxianwuju_111
10.170.109.202:   855  1 (UNLOCKED)  1 (ENABLED)   GNBDUFunction=1,NRCellDU=E11587835LSLDxianwuju_112
10.170.109.202:   856  1 (UNLOCKED)  1 (ENABLED)   GNBDUFunction=1,NRCellDU=E11587835LSLDxianwuju_113
10.170.109.202: ===================================================================================
10.170.109.202: Total: 3 MOs'''

result=[]
AdmState=re.findall('\d\d\d  \d \((.*?)\)  \d ',content,re.S)
OpState=re.findall('\d\d\d  \d \(.*?\)  \d \((.*?)\)   GNBDUFunction=1,NRCellDU=',content,re.S)
cell=re.findall('GNBDUFunction=1,NRCellDU=(.*?_\d\d\d)',content,re.S)

for i in range(len(AdmState)):
    result1={'AdmState':AdmState[i],'OpState':OpState[i],'cell':cell[i]}
    result.append(result1)

print(result)

with open('cellstate.csv','w',encoding='UTF-8',newline='') as c:
    writer=csv.DictWriter(c,fieldnames=['AdmState','OpState','cell'])
    writer.writeheader()
    writer.writerows(result)
