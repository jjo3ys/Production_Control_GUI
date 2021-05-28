from tkinter import *
from tkinter import ttk
from itertools import combinations

import math
import tkinter.messagebox as msgbox

def calculate(factor, norm_factor):
    total_center = []
    for n in range(1, len(factor)+1):
        t_cost = []
        centers = list(combinations(range(len(factor)), n))
        for center in centers:
            high = sorted(factor, key = lambda x:x[-1])

        # for m in range(len(factor)):  

        #     cost = 0
        #     market = factor
        #     center = factor[m]

        #     for o in market:
        #         distance = math.sqrt((float(center[0][0])-float(o[0][0]))**2+(float(center[0][1])-float(o[0][1]))**2)
        #         o_cost = distance*o[1]*o[2]*norm_factor[3]
        #         cost += o_cost

        #     t_cost.append(cost)

        # sort_list = sorted(t_cost)
        # center = t_cost.index(sort_list[0])
        # total_center.append([center, sort_list[0]])
        
            
def insert(factor, i, entx, enty, entd, entc, norm_factor):   
    try:
        factor[i][0][0] = float(entx.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        factor[i][0][1] = float(enty.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        factor[i][1] = float(entd.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        factor[i][2] = float(entc.get())
        # if factor[-1][-1] == '':
        #     define(factor, i+1)   
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')
    factor[i][3] = factor[i][1]*factor[i][2]

    if i == len(factor)-1:
        calculate(factor, norm_factor) 

def define_(factor, i, norm_factor):
    if i == 0:
        Label(root, text = '').grid(row = 2, column = 0)
        Label(root, text = 'x좌표').place(x = 90, y = 80)
        Label(root, text = 'y좌표').place(x = 160, y = 80)
        Label(root, text = '시간단위당\n 수요량').place(x = 210, y = 80)
        Label(root, text = '단위당\n수송운임').place(x = 280, y = 80)

    else:
        Label(root, text = '시장{0}'.format(i)).place(x = 30, y = 80+40*i)
        entx = Entry(root, width = 10)
        entx.place(x = 70, y = 80+40*i)
        enty = Entry(root, width = 10)
        enty.place(x = 140, y = 80+40*i)
        entd = Entry(root, width = 10)
        entd.place(x = 210, y = 80+40*i)
        entc = Entry(root, width = 10)
        entc.place(x = 280, y = 80+40*i)
        Button(root, text = '입력', command = lambda: insert(factor, i-1 ,entx, enty, entd, entc, norm_factor)).place(x = 350, y = 80+40*i-5)

def get_num(entn, entb, entc, entk):
    try:
        num = int(entn.get())
        factor = [[['',''],'','', ''] for i in range(num)]
    except:
        msgbox.showwarning('경고', '1 이상의 자연수를 입력해주세요')
    
    try:
        year_expense = int(entb.get())
    except:
        msgbox.showwarning('경고', '1 이상의 자연수를 입력해주세요')
    
    try:
        year_stock = int(entc.get())
    except:
        msgbox.showwarning('경고', '1 이상의 자연수를 입력해주세요')
    
    try:
        K = int(entk.get())
    except:
        msgbox.showwarning('경고', '1 이상의 자연수를 입력해주세요')
    norm_factor = [num, float(year_expense), float(year_stock), float(K)]
    for i in range(num+1):
        define_(factor, i, norm_factor)
        i+=1
    
root = Tk()
root.title("물류센터 입지결정")
root.geometry("420x480")
root.resizable(False, True)

labeln = Label(root, text = '시장의 개수')
labeln.place(x=30, y=10)
labelb = Label(root, text = '연간 고정비')
labelb.place(x=110, y=10)
labelc = Label(root, text = '연간 재고\n관리비')
labelc.place(x=200, y=10)
labelk = Label(root, text = '축적치')
labelk.place(x=300, y=10)

entn = Entry(root, width = 5)
entn.place(x=35, y=40)
entb = Entry(root, width = 8)
entb.place(x=115, y=40)
entc = Entry(root, width = 8)
entc.place(x=205, y=40)
entk = Entry(root, width = 5)
entk.place(x=305, y=40)

num = Button(root, text = '입력', command = lambda: get_num(entn, entb, entc, entk))
num.place(x=350, y=35)

root.mainloop()