from tkinter import BOTH,Tk,Canvas,Button
from tkinter.messagebox import YES
root = Tk()
root.title("画16*16格子")
root.geometry('600x600')
canvas=Canvas(root,background='white')
canvas.pack(expand=YES,fill=BOTH)
for i in range(1,18):  
    canvas.create_line(i*30,30,i*30,510,width=2,fill='black')  
for i in range(1,18):
    canvas.create_line(30,i*30,510,i*30,width=2,fill='black')  
def button_1():
  canvas.create_text(40,40,text="交")
def button_2():
  canvas.create_text(140,140,text="大")
btn1=Button(root,text="button1",width=10,command=button_1)
btn2=Button(root,text="button2",width=10,command=button_2)
btn1.pack()
btn2.pack()
root.mainloop()
