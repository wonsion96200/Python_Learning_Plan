#!/usr/bin/env python
# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# File Name:    Hget 中提取数据
# Author:       Dong Xu D
# Created:      8/16/2019 4:24 PM
#-------------------------------------------------------------------------------
import os
import datetime
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox as mBox
from tkinter import filedialog
import time
global current_time
current_time=time.strftime("%Y_%m_%d", time.localtime())
win = tk.Tk()
win.title('HGET_TOOL')
win.geometry('800x400+150+150')

#创建文本窗体
OutputDisplayArea = scrolledtext.ScrolledText(win, width=60, height=5, wrap=tk.WORD)
current_time = datetime.datetime.now().strftime('%H:%M:%S\t')
info = 'SZ Test\n'
info += '%s Program running......\n' % current_time
OutputDisplayArea.insert(tk.END, info)
OutputDisplayArea.grid(column=0, row=2, padx=4, pady=4,sticky='WE', columnspan=5)
content=OutputDisplayArea.get('1.0','end-1c')
print(content)


text = tk.Text(win,width = 50,height = 20)
text.grid(column=0, row=4, padx=4, pady=4,sticky='WE', columnspan=5)

content='这个表示字符串，将输出结果显示再文本框内'
global rncid
global path
def select_file():
    text.delete(0.0,tk.END)
    text.insert(tk.INSERT,content)

butten1=tk.Button(win,text="选择文本",command=select_file,width=12,height=3)
butten1.grid(column=6,row=2,padx=10,pady=10,sticky=tk.W)
win.mainloop()
