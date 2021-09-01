
import re
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def texttolist(content,file):
    testlist=re.findall(content, file)
    return testlist

def get_filelist(dir,Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)
    return Filelist

if __name__ == '__main__':

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()

    file_list = get_filelist(file_path, [])
#    print(file_list)
    RelationListTotal = pd.DataFrame()
    for e in file_list:
        with open(e, "r") as fileRead:
            logContent = fileRead.read()
            fileRead.close()

        #NRCellRelation = [["NRCellCU", "NRCellRelation"]]

        #for line in logContent:
        #    if re.search('[0-9].*GNBCUCPFunction=.*,NRCellCU=.*,NRCellRelation=', line):
        #        print(line)
        #        print(line.split('NRCellCU=')[1].split(',')[0])
        #        print(line.split('NRCellRelation=')[1])
        #        NRCellRelation.append([line.split('NRCellCU=')[1].split(',')[0], line.split('NRCellRelation=')[1].split()[0]])

        #findRelation = re.findall('[0-9].*GNBCUCPFunction=.*,NRCellCU=.*,NRCellRelation=.*', str(logContent))

        #for i in findRelation:
        #    NRCellRelation.append([i.split('NRCellCU=')[1].split(',')[0], i.split('NRCellRelation=')[1].split()[0]])


        #NRCellRelation_pd = pd.DataFrame(NRCellRelation)

        #print(NRCellRelation_pd)



        #df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
        # "date":pd.date_range('20130102', periods=6),
        #  "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
        # "age":[23,44,54,32,34,32],
        # "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
        #  "price":[1200,1111,2133,5433,2222,4432]},
        #  columns =['id','date','city','category','age','price'])

        #print(df)

        RelationList = pd.DataFrame(columns=['Serving_SiteId', 'Serving_CellName', 'Neighbor_CellName'])


        findRelation = re.findall('[0-9].*GNBCUCPFunction=.*,NRCellCU=.*,NRCellRelation=.*', str(logContent))
        row = 0
        for i in findRelation:
            if i.split('NRCellCU=')[1].split(',')[0].split('-')[0] != i.split('NRCellRelation=')[1].split()[0].split('-')[0]:
                RelationList.loc[row] = [i.split('NRCellCU=')[1].split(',')[0].split('-')[0][1:], i.split('NRCellCU=')[1].split(',')[0],
                                         i.split('NRCellRelation=')[1].split()[0]]
                row += 1

        file = logContent
        file_split = file.split('hget ')
        # print(file_split)
        externalpart = texttolist('ExternalNRCellCU=(.*)', file_split[2])
        # print(externalpart)
        externalpart = externalpart[1:]
        newexternalpart = []
        for a in externalpart:
            a = a.replace('NRNetwork=1,NRFrequency=', ' ').split()
            newexternalpart.append(a)
        # print(newexternalpart)
        for x in newexternalpart:
            x[0] = x[0][1:9]
            temp = x[3].split('-')
            del x[3]
            x.insert(3, temp[0])
            x.insert(6, temp[4])
            x.insert(7, temp[3])
            x.insert(8, temp[2])
            x.insert(9, temp[1])
            temp1 = x.pop(1)
            x.insert(3, temp1)
        # print(newexternalpart)
        external_df = pd.DataFrame(newexternalpart)
        external_df.columns = ['Neighbor_SiteId', 'Neighbor_CellName', 'Neighbor_arfcn', 'Neighbor_Cellid',
                               'Neighbor_PCI', 'Neighbor_TAC', 'smtcScs', 'smtcPeriodicity', 'smtcOffset',
                               'smtcDuration']
        #
#        print(external_df)

        externalpart1 = texttolist('ExternalGNBCUCPFunction=(.*)', file_split[1])
        externalpart1 = externalpart1[1:]
        # print(externalpart1)
        newexternalpart1 = []
        for a in externalpart1:
            a = a.split()
            newexternalpart1.append(a)
            # print(newexternalpart1)

        for x in newexternalpart1:
            x[3] = x[3] + x[4]
            x.pop(4)
        # print(newexternalpart1)
        external_df1 = pd.DataFrame(newexternalpart1)
        external_df1.columns = ['Neighbor_SiteId', 'Neighbor_gNodeBID', 'Neighbor_gNodeBIdLength', 'Neighbor_PLMN']
#        print(external_df1)
        pdfinal = pd.merge(external_df, external_df1, on='Neighbor_SiteId', how='left')
        pdfinal=pdfinal[['Neighbor_SiteId', 'Neighbor_gNodeBID','Neighbor_CellName', 'Neighbor_arfcn','Neighbor_gNodeBIdLength',
                         'Neighbor_Cellid','Neighbor_PCI', 'Neighbor_TAC','Neighbor_PLMN', 'smtcScs','smtcPeriodicity',
                         'smtcOffset', 'smtcDuration']]
#        print(pdfinal)

        RelationList = RelationList.merge(pdfinal, on='Neighbor_CellName', how='left')
        RelationList = RelationList[['Serving_SiteId', 'Serving_CellName', 'Neighbor_SiteId', 'Neighbor_gNodeBID',
                                     'Neighbor_CellName', 'Neighbor_arfcn','Neighbor_gNodeBIdLength', 'Neighbor_Cellid',
                                     'Neighbor_PCI', 'Neighbor_TAC','Neighbor_PLMN', 'smtcScs','smtcPeriodicity',
                                     'smtcOffset', 'smtcDuration']]
#        print(RelationList)
        RelationListTotal = pd.concat([RelationListTotal, RelationList], axis=0)

#install openpyxl to write into xlsx, xlwt to write into xls
    RelationListTotal.to_excel('NeighborRelation_check_BJCU.xlsx', header=True, index=False)

