# 设计文档
## 程序实现说明及运行
要求:实现五子棋
首先，先定义五子棋的窗口
```python
from tkinter import Tk,Label,Button,Canvas,StringVar
import tkinter.messagebox

root=Tk()
root.title("五子棋")
root.geometry('800x600')
```
接着，利用canvas函数画出14x14棋盘。其中利用canvas.bind函数，<Button-1>表示鼠标左键，每次点击鼠标左键都会触发chess_moving函数。
```python
canvas=Canvas(root,background='tan1',width=510, height=510)
canvas.bind("<Button-1>",chess_moving)
canvas.grid(row=0,column=0)
```
因为是14x14棋盘，共有15条横线及竖线，利用canvas内建的create_line函数分别绘出这些直线。
```python
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
```
棋盘上有五个交点，计算得知这些点的坐标分别是(115,115),(355,115),(115,355),(235,235),(355,115)。
为使交点落在线与线相交的位置，起始坐标与终点坐标分别-3，+3。利用canvas内建的create_oval函数画交点。
```python
canvas.create_oval(112,112,118,118,fill="black") 
canvas.create_oval(352,112,358,118,fill="black") 
canvas.create_oval(112,352,118,358,fill="black") 
canvas.create_oval(232,232,238,238,fill="black") 
canvas.create_oval(352,352,358,358,fill="black") 
```
定义全局变量，color_number为1表示黑棋，0表示白棋，size表示棋盘边缘大小，stop为0表示没有一方获胜，1表示有一方获胜。
chess表示所有棋子坐标列表
```python
color_number=1 
size=15
stop=0
chess=[[0 for i in range(size+1)] for i in range(size+1)]
```
定义chess_moving函数，以确定棋子坐标并让棋子落在棋盘点上。
```python
def chess_moving(event):
    global color_number
```
为了让棋子下在十字中间，我们需要对点击坐标进行修改，对X和Y求余数，
如果大于15，就除于30后+1，小于15就直接除于30。其中30是两条线之间的长度。
```python
    if event.x %30>15:    
        event.x=event.x//30+1 
    else:
        event.x=event.x//30
    if event.y%30>15:
        event.y=event.y//30+1
    else:
        event.y=event.y//30
```
然后将得到的event.x和event.y进行边缘检测，注意不要超出棋谱范围。如果超出边缘就落在边缘位置。确定棋子的起始坐标与终点坐标。   
```python
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
```
为了让棋子不重复覆盖，创建一个全为0的二维数组。在点击的坐标后再设置为相应的1和2（1代表黑棋，2代表白棋），只有该坐标为0的时候才能下棋子，这样就能不重复了。gameover函数之后介绍。
```python
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
```
定义info函数，作用是在出现一方赢家时，弹出窗口提示游戏结束。此时stop为1。
```python
def info(): 
    global stop
    tkinter.messagebox.showinfo("","Game over")
    stop=1
```
定义gameover函数，判断是否有五个同色棋子连在一起，共有八个方向判断，依次为左右上下，左斜右斜。左斜又可拆成左上右下，同理右斜拆成左下右上。
初始化count为0，遍历各个方向若等于点击的坐标，则加一。若count=5则弹出窗口提示。
```python
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
```
处理左斜及右斜时，使用zip函数把两个坐标打包成一个数组。
```python
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
```
定义退出游戏的按钮，提示黑棋先手的标签。
```python
quit=Button(root,text="退出游戏",command=root.quit)
quit.grid(row=6,column=1)
var=StringVar()
piece_canvas=Canvas(root,width=200,height=50)
piece_canvas.grid(row=0,column=1)
piece_canvas.create_oval(90,20,110,40,fill="black")
var.set("黑棋先手")
label=Label(root,textvariable=var,font=("宋体",16))
label.grid(row=1,column=1)
```
程序运行
```python
root.mainloop()
 ```