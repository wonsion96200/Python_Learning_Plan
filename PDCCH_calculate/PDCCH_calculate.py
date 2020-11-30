# import win32ui
# bbCellIndex=0代表Pcell，bbCellIndex=2代表Scell：
# 假设Pcell上noOfCce=8的次数出现了1000次，noOfCce=1的次数出现了10000次，那么Pcell上计算（8*1000+1*10000）/（1000+10000）=18000/11000=1.636。
# dlg=win32ui.CreateFileDialog(1)
import os
import re
import tkinter as tk
from tkinter import filedialog



def get_filelist(dir,Filelist):
  newDir = dir
  if os.path.isfile(dir):
    Filelist.append(dir)
  elif os.path.isdir(dir):
    for s in os.listdir(dir):
      newDir=os.path.join(dir,s)
      get_filelist(newDir,Filelist)
  return Filelist

critercalP8 = " bbCellIndex=0(.*?)noOfCce=8 "
critercalP1 = " bbCellIndex=0(.*?)noOfCce=1 "
critercalS8 = " bbCellIndex=2(.*?)noOfCce=8 "
critercalS1 = " bbCellIndex=2(.*?)noOfCce=1 "


if __name__ == '__main__':

    root =tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    #print(file_path)
    #file_path='C:/Users/ewaglee/Desktop/Python/Request/Gavin/file'
    file_list=get_filelist(file_path,[])
    #print(file_list)
    for e in file_list:
        forder_name=re.findall("_(.*?)\\\\", e)
        #print(forder_name)
        #scrf1 = open(e, 'r')
        #outf1 = open(e + '_pcell.txt', 'w+')
        #outf2 = open(e + '_scell.txt', 'w+')

        scrf1 = open(e, 'r').read()
        P8 = len(re.findall(critercalP8, scrf1))
        P1 = len(re.findall(critercalP1, scrf1))
        S8 = len(re.findall(critercalS8, scrf1))
        S1 = len(re.findall(critercalS1, scrf1))

        # print(P8)
        # print(P1)
        # print(S8)
        # print(S1)

        PCell_expect_result= (8 * P8 + 1 * P1)/(P8+P1)
        Scell_expect_result = (8 * S8 + 1 * S1) / (S8 + S1)
        print('{}_PCell的PDCCH开销是{:.8f},  SCell的PDCCH开销是{:.8f}'.format(forder_name,PCell_expect_result, Scell_expect_result))








