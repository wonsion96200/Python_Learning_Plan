# List missing ROP file name
import re
import os
import sys

with open("All_ROP_Files_20201012.txt", "r") as allRopFile:
    allRop = allRopFile.read()
    allRopFile.close()

#with open("result.txt", "a+") as result:


with open("Nodelist.txt", "r") as nodeList:
    for line in nodeList:
        node = line.strip()
        temp = re.findall(node + "_statsfile.xml", allRop) #check num. of lines for 1 node
        if len(temp) < 28:
            subNetwork = re.search("_SubNetwork=.*ManagedElement=" + node, allRop).group() #group()取匹配出的内容,re.search只查找一次
            subNetwork = re.sub('_', '', subNetwork) #replace _ to empty
            print(node)
            startTime = 200
            for i in range(1, 28):
                if i%4 == 0:
                    findStr = node + "/A20201012.0" + str(startTime) + "+0100-0" + str(startTime + 55)
                else:
                    findStr = node + "/A20201012.0" + str(startTime) + "+0100-0" + str(startTime + 15)
                j = 0
                if findStr in allRop: #如果某一个rop文件能在allrop里找到，J=1
                    j = 1
                if j == 0:
                    print(subNetwork + "/" + re.split("\/", findStr)[1] + "_" + subNetwork + "_statsfile.xml")
                if i%4 == 0:
                    startTime = startTime + 55
                else:
                    startTime = startTime + 15

nodeList.close()
