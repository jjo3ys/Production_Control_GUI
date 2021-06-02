from tkinter import *

import math
import tkinter.messagebox as msgbox

def reset(root):                                                                        #다시 시작
    root.destroy()
    main()

def calculate(element, base_element):
    copy = sorted(element, key = lambda x: -(x[1]*x[2]))                                #연간 수요량 X 단위당 수송비가 높은 순으로 정렬
    total_cost = []                                                                     #입지의 개수마다 최소 총 비용과 수송흐름을 저장할 리스트

    for n in range(1, len(element)+1):                                                  #1에서부터 총 시장의 개수 까지 입지의 개수를 설정
        center = copy[:n]                                                                   #정렬된 리스트에서 상위 n개를 입지로 지정
        market = copy[n:]                                                                   #정렬된 리스트에서 n번째 부터 수송흐름이 이루어질 시장으로 지정
        flow = []                                                                           #수송흐름과 총 수송비를 저장할 리스트

        for c in center:                                                                #모든 센터와 모든 시장간의 수송비를 계산
            cost = 0
            for m in market:
                distance = math.sqrt((c[0][0] - m[0][0])**2 + (c[0][1] - m[0][1])**2)       #유클리디안 거리공식
                cost = distance * m[1] * m[2] * base_element[3]                             #수송비 = 거리*연간수요량*단위당 수송비*축적치
                flow.append([element.index(c)+1, element.index(m)+1, cost])                 #센터와 다른 시장간의 수송흐름과 수송비를 저장

        if n == 1:                                                                      #입지의 개수가 1일때는 단일설비 입지 문제를 적용 
            cost = 0                                                                    #단, 연간 수요량 X 단위당 수송비가 높은 시장을 입지로 적용
            for f in flow:
                cost += f[2]                                                                #총 수송비는 모든 시장간의 수송비를 합한값

            center = element.index(center[0])+1                                             #입지의 개수가 1일때 수송흐름은 입지를 제외한 모든 시장과의 흐름이므로 
            flow = [[center, i]for i in range(1, len(element)+1)]                           #입지와 모든 시장간의 흐름을 생성한뒤,
            del flow[center-1]                                                              #입지와 입지로 선정된 시장간의 흐름을 삭제
            cost = cost + base_element[1] + base_element[2]                                 #총 비용은 수송비 + 고정비 + 재고관리비
            total_cost.append([[center], flow, round(cost, 2)])                             #입지개수별 수송비, 수송흐름을 리스트에 추가

        else:                                                                           #입지의 개수가 2이상일 경우
            flow.sort(key = lambda x: x[2])                                                 #수송흐름과 수송비가 저장된 리스트를 수송비가 적은 순으로 정렬
            dummy = []                                                                      #시장 중복 방지를 위한 dummy 리스트
            set = []                                                                        #따로 수송흐름을 저장할 리스트
            cent = []                                                                       #입지로 선정된 시장의 번호를 저장할 리스트
            cost = 0

            for c in center:                                                                #입지로 선정된 시장의 번호를 추가
                cent.append(element.index(c)+1)
            cent.sort()                                                                   

            for f in flow:                                                                  #수송비가 적은 순으로 하나씩 불러옴
                if f[1] not in dummy:                                                           #시장이 dummy 리스트에 없을 시에만 실행 이때 f = [입지, 시장, 수송비]
                    dummy.append(f[1])                                                              #dummy에 해당 시장을 저장
                    set.append([f[0], f[1]])                                                        #수송흐름을 저장
                    cost += f[2]                                                                    #총 수송비

                    if len(dummy) == len(market):                                                       #dummy에 저장된 시장의 개수가 수송흐름이 이루어질 시장의 개수가 같다는 것은 
                        break                                                                           #최적으로 수송흐름이 정해졌다는 것을 의미

            set.sort(key = lambda x: x[0])
            cost = cost + base_element[1] * n + base_element[2] * math.sqrt(n)          #입지의 개수가 2이상일 경우 총 비용은 총수송비 + 고정비 * 입지의 개수 + 관리비 * 입지의개수의 제곱근
            total_cost.append([cent, set, round(cost, 2)])                              #입지개수별 수송비, 수송흐름을 리스트에 추가
    
    return total_cost
            
def insert(element, i, entx, enty, entd, entc, base_element, root):   
    try:                                                                                #list의 index는 0부터 시작하기 때문에 i-1을 사용
        element[i-1][0][0] = float(entx.get())                                          #x좌표 입력
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        element[i-1][0][1] = float(enty.get())                                          #y좌표 입력
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        element[i-1][1] = float(entd.get())                                             #연간 수요량 입력
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    try:
        element[i-1][2] = float(entc.get())                                             #단위당 수송비 입력
    except:
        msgbox.showwarning('경고', '실수를 입력해주세요')

    if element[-1][-1] == '':                                                           #시장의 개수에 따라 지정된 list에 모든 요소가 다 찰때까지 입력하는 함수 실행
        define(element, i+1, base_element, root) 

    else:
        total = calculate(element, base_element)                                        #입지 개수별 최적의 수송흐름과 최소 총비용
        Label(root, text = '입지 개수 별 최적 입지').place(x=35,y=80+(i+1)*40)
        Label(root, text = '입지 개수').place(x=10, y=60+(i+2)*40)
        Label(root, text = '입지 위치').place(x=80, y=60+(i+2)*40)
        Label(root, text = '수송 흐름').place(x=160, y=60+(i+2)*40)
        Label(root, text = 'total cost').place(x=250, y=60+(i+2)*40)

        for j in range(1, len(total)+1):                                                #row마다 입지 개수, 선정된 입지의 시장번호, 수송흐름, 총 비용을 출력
            Label(root, text = '{0}개'.format(j)).place(x=25, y=50+(i+j)*60)
            Label(root, text = 'M{0}'.format(str(total[j-1][0]).replace('[', '').replace(']', ''))).place(x=80, y=50+(i+j)*60)   
            frame = Frame(root)
            frame.place(x=150, y=40+(i+j)*60)
            lbox = Listbox(frame, width=10, height=1)
            lbox.pack(side='left', fill='y')
            scroll = Scrollbar(frame, orient='vertical')
            scroll.config(command = lbox.yview)
            scroll.pack(side='right', fill='y')

            for s in total[j-1][1]:    
                lbox.insert(END, 'M{0}->M{1}'.format(s[0], s[1]))
        
            
            Label(root, text = '{0}'.format(total[j-1][2])).place(x=250, y=60+(i+j)*60)

        total.sort(key = lambda x: x[2])                                                #입지 개수 별 최적 수송흐름과 최소 총 비용의 list를 총 비용이 적은 순으로 정렬하여 
        Label(root, text = '최종 최적입지').place(x=35,y=60+(i+1+j)*60)                  #가장 총비용이 적은 입지를 총 비용과 함께 출력
        Label(root, text = 'M{0}'.format(str(total[0][0]).replace('[', '').replace(']', ''))).place(x=45, y=100+(i+1+j)*60)   
        Label(root, text = 'total cost:{0}'.format(total[0][2])).place(x=150, y=100+(i+1+j)*60)   

def define(element, i, base_element, root):
    if i == 0:                                                                          #각 칸에 들어가야 하는 것에 대한 설명
        Label(root, text = 'x좌표').place(x = 90, y = 80)
        Label(root, text = 'y좌표').place(x = 160, y = 80)
        Label(root, text = '시간단위당\n 수요량').place(x = 210, y = 80)
        Label(root, text = '단위당\n수송운임').place(x = 290, y = 80)
        define(element, i+1, base_element, root)

    else:
        Label(root, text = 'M{0}'.format(i)).place(x = 30, y = 80+40*i)
        entx = Entry(root, width = 10)                                                  #x좌표 입력 칸
        entx.place(x = 70, y = 80+40*i)
        enty = Entry(root, width = 10)                                                  #y좌표 입력칸
        enty.place(x = 140, y = 80+40*i)
        entd = Entry(root, width = 10)                                                  #연간 수요량 입력칸
        entd.place(x = 210, y = 80+40*i)
        entc = Entry(root, width = 10)                                                  #단위당 수송비 입력칸
        entc.place(x = 280, y = 80+40*i)
        Button(root, text = '입력', command = lambda: insert(element, i ,entx, enty, entd, entc, base_element, root)).place(x = 350, y = 80+40*i-5)

def get_num(entn, entb, entc, entk, root):
    try:
        num = int(entn.get())                                                           #시장의 개수
        root.geometry("420x{0}".format(240+120*num))                                    #User가 입력한 시장의 개수에 따라 창의 크기가 달라짐
        element = [[['',''],'',''] for i in range(num)]                                 #User가 입력한 시장의 개수에 따라 list크기를 지정 
    except:                                                                             #이때 하나의 row마다 [x좌표, y좌표], 연간수요량, 단위당 수송비 가 들어감
        msgbox.showwarning('경고', '1 이상의 자연수를 입력해주세요')
    
    try:
        year_expense = float(entb.get())                                                #고정비
    except:
        msgbox.showwarning('경고', '0 이상의 실수를 입력해주세요')
    
    try:
        year_stock = float(entc.get())                                                  #재고관리비
    except:
        msgbox.showwarning('경고', '0 이상의 실수를 입력해주세요')
    
    try:
        K = float(entk.get())                                                           #축적치
    except:
        msgbox.showwarning('경고', '0 이상의 실수를 입력해주세요')

    base_element = [num, year_expense, year_stock, K]
    Button(root, text = 'Reset', command=lambda : reset(root)).place(x=350, y=80)

    define(element, 0, base_element, root)


def main():
    root = Tk()
    root.title("물류센터 입지결정")
    root.geometry("420x120")
    root.resizable(False, False)

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