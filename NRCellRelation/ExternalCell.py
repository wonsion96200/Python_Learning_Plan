import re
import os
import pandas as pd

def texttolist(content,file):
    testlist=re.findall(content, file)
    return testlist


if __name__ == '__main__':
    # file_list=get_filelist(file_path,[])
    pd.set_option('display.width', 300)  # 数据显示总宽度
    pd.set_option('max_rows', 100)  # 显示最多行数，超出该数以省略号表示
    pd.set_option('max_columns', 200)  # 显示最多列数，超出该数以省略号表示
    pd.set_option('max_colwidth', 50)  # 设置单列的宽度，用字符个数表示，单个数据长度超出该数时以省略号表示

    file_list=r'BJ308687.log'
    # print(file_list)

    # for e in file_list:
    e = file_list

    file = open(e, 'r').read()
    file_split=file.split('hget ')
    # print(file_split)
    externalpart = texttolist('ExternalNRCellCU=(.*)',file_split[2])
    # print(externalpart)
    externalpart=externalpart[1:]
    newexternalpart = []
    for a in externalpart:
        a = a.replace('NRNetwork=1,NRFrequency=', ' ').split()
        newexternalpart.append(a)
    # print(newexternalpart)
    for x in newexternalpart:
        x[0]=x[0][1:9]
        temp=x[3].split('-')
        del x[3]
        x.insert(3,temp[0])
        x.insert(6, temp[4])
        x.insert(7, temp[3])
        x.insert(8, temp[2])
        x.insert(9, temp[1])
        temp1=x.pop(1)
        x.insert(3,temp1)
    # print(newexternalpart)
    external_df=pd.DataFrame(newexternalpart)
    external_df.columns = ['Neighbor_SiteId', 'Neighbor_CellName', 'Neighbor_arfcn', 'Neighbor_Cellid','Neighbor_PCI', 'Neighbor_TAC', 'smtcScs','smtcPeriodicity', 'smtcOffset', 'smtcDuration']
    #
    print(external_df)


    externalpart1 = texttolist('ExternalGNBCUCPFunction=(.*)', file_split[1])
    externalpart1 = externalpart1[1:]
    # print(externalpart1)
    newexternalpart1=[]
    for a in externalpart1:
        a = a.split()
        newexternalpart1.append(a)
        # print(newexternalpart1)

    for x in newexternalpart1:
        x[3]=x[3]+x[4]
        x.pop(4)
    # print(newexternalpart1)
    external_df1 = pd.DataFrame(newexternalpart1)
    external_df1.columns = ['Neighbor_SiteId','Neighbor_gNodeBID','Neighbor_gNodeBIdLength','Neighbor_PLMN']
    print(external_df1)
    pdfinal=pd.merge(external_df,external_df1,on='Neighbor_SiteId',how='left')
#    pdfinal=pdfinal[['Neighbor_SiteId', 'Neighbor_gNodeBID','Neighbor_CellName', 'Neighbor_arfcn','Neighbor_gNodeBIdLength', 'Neighbor_Cellid','Neighbor_PCI', 'Neighbor_TAC','Neighbor_PLMN', 'smtcScs','smtcPeriodicity', 'smtcOffset', 'smtcDuration']]
    print(pdfinal)

# external_df.columns = ['NeighborSiteId','NeighborCellid','NeighborCellName','Neighborarfcn','smtcScs','smtcPeriodicity','smtcOffset','smtcDuration','NeighborPCI','NeighborTAC']
    #





