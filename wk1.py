from tkinter import BOTH,Tk,Canvas
from tkinter.messagebox import YES
root = Tk()
root.title("画4*4格子")
root.geometry('600x600')
canvas=Canvas(root,background='white')
canvas.pack(expand=YES,fill=BOTH)
for i in range(1,6):  
    canvas.create_line(i*30,30,i*30,150,width=2,fill='black')  #竖线时，x轴相等
for i in range(1,6):
    canvas.create_line(30,i*30,150,i*30,width=2,fill='black')  #横线时，y轴相等
root.mainloop()

