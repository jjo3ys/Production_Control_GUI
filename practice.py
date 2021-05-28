from tkinter import *

root=Tk()
root.geometry('600x480')
scrollbar=Scrollbar(root)
scrollbar.grid(row = 3, column = 3, st)

mylist=Listbox(root,yscrollcommand=scrollbar.set)

for line in range(100):

    mylist.insert(END,"This is line number " + str(line))

mylist.grid(row = 0, column = 0)

scrollbar.config(command=mylist.yview)

mainloop()