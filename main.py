from tkinter import *
from tkinter import ttk
from itertools import combinations

import math
import tkinter.messagebox as msgbox
def reset(root):
    root.destroy()
    main()

def calculate(factor, norm_factor):
    c_factor = sorted(factor, key = lambda x: -x[-1])
    total_cost = []

    for n in range(1, len(factor)+1):
        center = c_factor[:n]
        market = c_factor[n:]
        flow = []

        for c in center:
            cost = 0
            for m in market:
                distance = math.sqrt((float(c[0][0])-float(m[0][0]))**2+(float(c[0][1])-float(m[0][1]))**2)
                cost = distance * m[3] * norm_factor[3]
                flow.append([factor.index(c)+1, factor.index(m)+1, cost])

        if n == 1:
            cost = 0
            for f in flow:
                cost += f[2]    

            center = factor.index(center[0])+1
            flow = [[center, i]for i in range(1, len(factor)+1)]
            del flow[center-1]
            cost = cost + norm_factor[1] + norm_factor[2]
            total_cost.append([[center], flow, round(cost, 2)])

        else:
            flow.sort(key = lambda x: x[2])
            dummy = []
            set = []
            cent = []
            cost = 0

            for c in center:
                cent.append(factor.index(c)+1)
            cent.sort()

            for f in flow:  
                if f[1] not in dummy:
                    dummy.append(f[1])
                    set.append([f[0], f[1]])
                    cost += f[2]

                    if len(dummy) == n:
                        break
            set.sort(key = lambda x: x[0])
            cost = cost + norm_factor[1] * n + norm_factor[2] * math.sqrt(n)
            total_cost.append([cent, set, round(cost, 2)])
    
    return total_cost
            
def insert(factor, i, entx, enty, entd, entc, norm_factor, root):   
    try:
        factor[i-1][0][0] = float(entx.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        factor[i-1][0][1] = float(enty.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        factor[i-1][1] = float(entd.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        factor[i-1][2] = float(entc.get())
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    factor[i-1][3] = factor[i-1][1] * factor[i-1][2]
    if factor[-1][-1] == '':
        define_(factor, i+1, norm_factor, root) 

    if i == len(factor):
        total = calculate(factor, norm_factor) 
        Label(root, text = '입지 개수 별 최적 입지').place(x=35,y=80+(i+1)*40)
        Label(root, text = '입지 개수').place(x=10, y=60+(i+2)*40)
        Label(root, text = '입지 위치').place(x=80, y=60+(i+2)*40)
        Label(root, text = '수송 흐름').place(x=160, y=60+(i+2)*40)
        Label(root, text = 'total cost').place(x=250, y=60+(i+2)*40)

        for j in range(1, len(total)+1):
            Label(root, text = '{0}개'.format(j)).place(x=25, y=60+(i+j)*60)
            Label(root, text = 'M{0}'.format(str(total[j-1][0]).replace('[', '').replace(']', ''))).place(x=80, y=60+(i+j)*60)   
            frame = Frame(root)
            frame.place(x=150, y=60+(i+j)*60)
            lbox = Listbox(frame, width=10, height=1)
            lbox.pack(side='left', fill='y')
            scroll = Scrollbar(frame, orient='vertical')
            scroll.config(command = lbox.yview)
            scroll.pack(side='right', fill='y')

            if total[j-1][1] != []:
                for s in total[j-1][1]:    
                    lbox.insert(END, 'M{0}->M{1}'.format(s[0], s[1]))
            
            else:
                for s in total[j-1][0]:
                    lbox.insert(END, 'M{0} -> M{0}'.format(s))
            
            Label(root, text = '{0}'.format(total[j-1][2])).place(x=250, y=60+(i+j)*60)

        total.sort(key = lambda x: x[2])
        Label(root, text = '최종 최적입지').place(x=35,y=60+(i+1+j)*60)
        Label(root, text = 'M{0}'.format(str(total[0][0]).replace('[', '').replace(']', ''))).place(x=45, y=100+(i+1+j)*60)   
        Label(root, text = 'total cost:{0}'.format(total[0][2])).place(x=150, y=100+(i+1+j)*60)   
        Button(root, text = 'Reset', command=lambda : reset(root)).place(x=350, y=100+(i+1+j)*60)

def define_(factor, i, norm_factor, root):
    if i == 0:
        Label(root, text = 'x좌표').place(x = 90, y = 80)
        Label(root, text = 'y좌표').place(x = 160, y = 80)
        Label(root, text = '시간단위당\n 수요량').place(x = 210, y = 80)
        Label(root, text = '단위당\n수송운임').place(x = 290, y = 80)
        define_(factor, i+1, norm_factor, root)

    else:
        Label(root, text = 'M{0}'.format(i)).place(x = 30, y = 80+40*i)
        entx = Entry(root, width = 10)
        entx.place(x = 70, y = 80+40*i)
        enty = Entry(root, width = 10)
        enty.place(x = 140, y = 80+40*i)
        entd = Entry(root, width = 10)
        entd.place(x = 210, y = 80+40*i)
        entc = Entry(root, width = 10)
        entc.place(x = 280, y = 80+40*i)
        Button(root, text = '입력', command = lambda: insert(factor, i ,entx, enty, entd, entc, norm_factor, root)).place(x = 350, y = 80+40*i-5)

def get_num(entn, entb, entc, entk, root):
    try:
        num = int(entn.get())
        root.geometry("420x{0}".format(240+120*num))
        factor = [[['',''],'','', ''] for i in range(num)]
    except:
        msgbox.showwarning('경고', '1 이상의 자연수를 입력해주세요')
    
    try:
        year_expense = float(entb.get())
    except:
        msgbox.showwarning('경고', '0 이상의 실수를 입력해주세요')
    
    try:
        year_stock = float(entc.get())
    except:
        msgbox.showwarning('경고', '0 이상의 실수를 입력해주세요')
    
    try:
        K = float(entk.get())
    except:
        msgbox.showwarning('경고', '0 이상의 실수를 입력해주세요')

    norm_factor = [num, year_expense, year_stock, K]

    #for i in range(num+1):
    define_(factor, 0, norm_factor, root)
        #i+=1

def main():
    root = Tk()
    root.title("물류센터 입지결정")
    root.geometry("420x120")
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
    entn.place(x=35, y=45)
    entb = Entry(root, width = 8)
    entb.place(x=115, y=45)
    entc = Entry(root, width = 8)
    entc.place(x=205, y=45)
    entk = Entry(root, width = 5)
    entk.place(x=305, y=45)

    num = Button(root, text = '입력', command = lambda: get_num(entn, entb, entc, entk, root))
    num.place(x=350, y=40)

    root.mainloop()

main()