from tkinter import Tk,Label,Button,Canvas,StringVar
import tkinter.messagebox

color_number=1 
size=15
stop=0
chess=[[0 for i in range(size+1)] for i in range(size+1)]

def chess_moving(event):
    global color_number
    if event.x %30>15:    
        event.x=event.x//30+1 
    else:
        event.x=event.x//30
    if event.y%30>15:
        event.y=event.y//30+1
    else:
        event.y=event.y//30   
    if event.x>size:
        event.x=size
    if event.y>size:
        event.y=size
    if event.x<1:
        event.x=1
    if event.y<1:
        event.y=1
    x1,y1=(event.x*30-15),(event.y*30-15)
    x2,y2=(event.x*30+15),(event.y*30+15)
    if stop==0:
        if chess[event.x][event.y]==0: 
            if color_number==1:
                canvas.create_oval(x1,y1,x2,y2,fill="black",tags="pieces")
                chess[event.x][event.y]=1
                gameover(event.x,event.y)
                color_number=0
            elif color_number==0:
                canvas.create_oval(x1,y1,x2,y2,fill="white",tags="pieces")
                chess[event.x][event.y]=2
                gameover(event.x,event.y)
                color_number=1
            
def info(): 
    global stop
    tkinter.messagebox.showinfo("","Game over")
    stop=1
            
def gameover(x,y):
    count=0
    for i in range(x,0,-1):   
        if chess[i][y]==chess[x][y]:
            count +=1
        else:
            break
    for i in range(x+1,16):  
        if chess[i][y]==chess[x][y]:
            count +=1
        else:
            break
    if count==5:
        info()
    count=0
    for i in range(y,0,-1):   
        if chess[x][i]==chess[x][y]:
            count +=1
        else:
            break
    for i in range(y+1,16):  
        if chess[x][i]==chess[x][y]:
            count +=1
        else:
            break
    if count==5:
        info()
    count=0

    for i,j in zip(range(x+1,17),range(y+1,16)):  
        if chess[i][j]==chess[x][y]:
            count +=1
        else:
            break
    for i,j in zip(range(x,0,-1),range(y,0,-1)):
        if chess[i][j]==chess[x][y]:
            count +=1
        else:
            break
    if count==5:
        info()
    count=0

    for i,j in zip(range(x-1,0,-1),range(y+1,16)): 
        if chess[i][j]==chess[x][y]:
            count +=1
        else:
            break
    for i,j in zip(range(x,17),range(y,0,-1)):    
        if chess[i][j]==chess[x][y]:
            count +=1
        else:
            break
    if count==5:
        info()
    count=0

root=Tk()
root.title("五子棋")
root.geometry('800x600')
canvas=Canvas(root,background='tan1',width=510, height=510)
canvas.bind("<Button-1>",chess_moving)
canvas.grid(row=0,column=0)
for i in range(0,15) :
          if i==0 or i==14 :
            canvas.create_line(25,25+i*30,25+420,25+i*30,width=2,fill='black')  
          else:
            canvas.create_line(25,25+i*30,25+420,25+i*30,width=1,fill='black')
for i in range(0,15):
          if i==0 or i==14:
            canvas.create_line(25+i*30,25,25+i*30,25+420,width=2,fill='black')  
          else:
            canvas.create_line(25+i*30,25,25+i*30,25+420,width=1,fill='black')
canvas.create_oval(112,112,118,118,fill="black") 
canvas.create_oval(352,112,358,118,fill="black") 
canvas.create_oval(112,352,118,358,fill="black") 
canvas.create_oval(232,232,238,238,fill="black") 
canvas.create_oval(352,352,358,358,fill="black") 

quit=Button(root,text="退出游戏",command=root.quit)
quit.grid(row=6,column=1)
var=StringVar()
piece_canvas=Canvas(root,width=200,height=50)
piece_canvas.grid(row=0,column=1)
piece_canvas.create_oval(90,20,110,40,fill="black")
var.set("黑棋先手")
label=Label(root,textvariable=var,font=("宋体",16))
label.grid(row=1,column=1)
root.mainloop()