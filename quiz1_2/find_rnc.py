#find_rnc
import re
f = open("RNC.log", "r")
nodename = f.readline().split('>')[0]
#print(nodename)
data = f.readlines()
numofcell = 0
cellinfo = []
for line in data:
    if "RncFunction=1" in line:
        rncid = line.split()[2]
#        print(rncid)
    if "UtranCell=" in line:
        numofcell = numofcell + 1
        temp = line.split()
#        print(temp)
        cellinfo.append([nodename,temp[0].split('=')[1],temp[0].split('=')[1][0:-1],temp[2],temp[1],temp[3].split(',')[0].split('=')[1],temp[3].split(',')[1].split('=')[1],temp[4],rncid,"4201-"+str(rncid)+"-"+str(temp[1])])
#        print(cellinfo)
#        cellname[numofcell-1] = temp[0].split('=')[1]
#        print(cellname[numofcell-1])
#        temp = re.split("=|,", line)

for i in cellinfo:
    print(' '.join(i))
#    for j in i:print(j,end = '')
#    print(cellinfo[i][0])

f.close()