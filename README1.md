# 设计文档
## 程序实现说明及运行
要求:实现俄罗斯方块游戏
首先，定义俄罗斯方块的窗口。
```python
from tkinter import Canvas, Label, Tk, messagebox
import random

root=Tk()
root.title("俄罗斯方块")
root.geometry("800x600")
```
利用canvas()函数画两个画布，第一个画布用来装俄罗斯方块的游戏界面，另一个装游戏玩法说明。接着利用label函数显示游戏玩法说明。
```python
canvas=Canvas(root,width=360,height=600)
canvas.grid(row=0,column=0)
canvas1=Canvas(root,width=200,height=600)
canvas1.grid(row=1,column=1)
label=Label(root,text="键盘↑旋转方块\n\n键盘←向左移\n\n键盘→向右移\n\n键盘↓放置方块",font=("宋体",16))
label.place(x=500,y=200)
```
初始化游戏参数，其中Size是格子的长度，Row是行数，Column是列数，FPS是定时的时间，score是得分。
```python
Size=30
Row=20
Column=12
FPS=500
score=0
```
定义draw_block函数画出单个俄罗斯方块，方块颜色默认为lightsteelblue。canvas是画板，cc是方块所在列，rr是方块所在行。
```python
def draw_block(canvas,cc,rr,color="lightsteelblue"):
    x0=cc*Size
    y0=rr*Size
    x1=cc*Size+Size
    y1=rr*Size+Size
    canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline="white",width=2)
```
定义draw_board函数画出所有空白方块。
```python
def draw_board(canvas,block_list):
    for i in range(Row):
        for j in range(Column):
            celltype=block_list[i][j]
            if celltype:
                draw_block(canvas,j,i,SHAPESCOLOR[celltype])
            else:
                draw_block(canvas,j,i)
```
画出各种形状的俄罗斯方块。建立字典SHAPES来记录各种形状，键是各种形状的字符串，值是对应的坐标列表。
同时建立字典SHAPESCOLOR来记录各种形状对应的颜色，键同上，值是颜色。
绘制形状时，x轴是列，y轴是行，取原点(0,0)为固定点，根据形状在x,y轴上衍生。如"田"方块，(0,0)为固定点时，向左衍生出(-1,0),向上衍生出(0,-1)再向左衍生出(-1,-1)。设定横坐标轴向右为正方向，纵坐标轴向下为正方向。
```python
SHAPES={
    "O":[(-1,-1),(0,-1),(-1,0),(0,0)],
    "S":[(-1,0),(0,0),(0,-1),(1,-1)],
    "Z":[(-1,-1),(0,-1),(0,0),(1,0)],
    "I":[(0,1),(0,0),(0,-1),(0,-2)],
    "L":[(-1,0),(0,0),(-1,-1),(-1,-2)],
    "J":[(-1,0),(0,0),(0,-1),(0,-2)],
    "T":[(-1,0),(0,0),(0,-1),(1,0)],
    }
SHAPESCOLOR={
    "O":"blue",
    "S":"red",
    "Z":"yellow",
    "I":"green",
    "L":"purple",
    "J":"orange",
    "T":"cyan",
    }
```
一个形状可以看成是多个方块组成，所以定义draw_shape函数来画出这些形状。cc是该形状设定的原点所在的列，rr是所在的行，cell_list是该形状各个方块相对自身所在位置。
```python
def draw_shape(canvas,cc,rr,cell_list,color="lightsteelblue"):
    for i in cell_list:
        cell_c,cell_r=i
        col=cell_c+cc
        rol=cell_r+rr
        #判断该位置方块在画板内部，在画板外部则不画出
        if 0<=cc<Column and 0<=rr<Row:
            draw_block(canvas,col,rol,color)
```
画好方块后，让游戏界面能动起来，即方块能移动，就需要定时刷新界面，并移动内部的俄罗斯方块。因此定义game_loop函数，每隔500毫秒刷新一次。
```python
def game_loop():
    root.update()
    global currentblock  #将当前的俄罗斯方块对象通过全局变量储存
    if currentblock is None:  #此时每次运行时会生成随机的俄罗斯方块
        newblock=generate_newblock()  #生成随机的俄罗斯方块
        draw_blockmoving(canvas,newblock)  #画出新生成的俄罗斯方块
        currentblock=newblock
        if not checkmove(currentblock,[0,0]):
            messagebox.showinfo("Game Over!","Your score is %s"%score)   #弹出窗口提示并显示得分
            root.destroy()
            return
    else:
        if checkmove(currentblock,[0,1]):  #判断能否向指定位置移动
            draw_blockmoving(canvas,currentblock,[0,1])  #向下画出新生成的方块
        else:  #无法移动，记入block_list
            saveblocktolist(currentblock)
            currentblock=None
            checkandclear()   #无法移动时，检查所有行能否被消除
    root.after(FPS,game_loop)

currentblock=None #将当前的俄罗斯方块初始化为空
```
定义draw_blockmoving函数使方块动起来，其中block是俄罗斯方块对象，direction是俄罗斯方块移动方向.
```python
def draw_blockmoving(canvas,block,direction=[0,0]):
    #建立字典(可看作一个俄罗斯方块对象)来储存某个俄罗斯方块的相关数据
    shapetype=block['kind']  #'kind'对应俄罗斯方块类型
    c,r=block['cr']          #'cr'对应横纵坐标
    cell_list=block['cell_list']  #对应俄罗斯方块的各个方格
    #移动前，先清除原有位置的俄罗斯方块，即用背景色画出原有的俄罗斯方块
    draw_shape(canvas,c,r,cell_list)
    #设定新位置参数
    dc,dr=direction
    new_c,new_r=c+dc,r+dr
    block['cr']=[new_c,new_r]
    #在新位置画出新的俄罗斯方块
    draw_shape(canvas,new_c,new_r,cell_list,SHAPESCOLOR[shapetype])
```
接下来就要随机生成任意形状的俄罗斯方块，定义generate_newblock函数。
```python
def generate_newblock():
    kind=random.choice(list(SHAPES.keys()))
    cr=[Column//2,0]  #使随机生成的俄罗斯方块在中间出现
    newblock={
        'kind':kind,  #此时'kind'是随机生成的kind
        'cell_list':SHAPES[kind],
        'cr':cr
    }
    return newblock
```
定义checkmove来判断方块是否能向指定位置移动，并固定该方块。若底下已有俄罗斯方块也不能移动。其中direction是移动方向。
```python
def checkmove(block,direction=[0,0]):
    cc,cr=block['cr']
    cell_list=block['cell_list']
    for i in cell_list:
        cell_c,cell_r=i
        c=cell_c+cc+direction[0]
        r=cell_r+cr+direction[1]
        if c<0 or c>=Column or r>=Row: #判断该位置是否超出右边界及下边界
            return False
        if r>=0 and block_list[r][c]:  #判断r不大于零使得新方块能向下移动，底下是否已有方块
            return False
    return True
```
因为要固定方块，所以添加一个变量block_list来记录已固定的俄罗斯，确保新生成的方块移动后不会覆盖旧的。
```python
block_list=[]
for i in range(Row):
    irow=[''for j in range(Column)]
    block_list.append(irow)
draw_board(canvas,block_list) #画出俄罗斯方块空白面板
```
关于确保新生成的方块不会覆盖旧的，定义saveblocktolist函数，记录已固定的方块。
```python
def saveblocktolist(block):
    shapetype=block['kind']
    cc,cr=block['cr']
    cell_list=block['cell_list']
    for i in cell_list:
        cell_c,cell_r=i
        c=cell_c+cc
        r=cell_r+cr
        block_list[r][c]=shapetype #在对应位置记下其类型
```
接着就是移动方块，定义horizontalmoveblock函数来水平移动方块。其中event参数对应键盘事件.
```python
def horizontalmoveblock(event):
    direction=[0,0]
    if event.keysym=='Left':
        direction=[-1,0]
    elif event.keysym=='Right':
        direction=[1,0]
    else:
        return
    global currentblock
    if currentblock is not None and checkmove(currentblock,direction):
        draw_blockmoving(canvas,currentblock,direction)  #根据键盘事件画出新的方块
```
能左右移动后，定义rotate函数来变换俄罗斯方块。
```python
def rotate(event):
    global currentblock
    if currentblock is None:
        return
    cell_list=currentblock['cell_list']
    rotate_list=[]
    for i in cell_list:
        cell_c,cell_r=i
        rotate_cell=[cell_r,-cell_c]
        rotate_list.append(rotate_cell)
    blockafterrotate={
        'kind':currentblock['kind'], 
        'cell_list':rotate_list,
        'cr': currentblock['cr']
    }
    if checkmove(blockafterrotate):
        cc,cr=currentblock['cr']
        draw_shape(canvas,cc,cr,currentblock['cell_list'])
        draw_shape(canvas,cc,cr,rotate_list,SHAPESCOLOR[currentblock['kind']])
        currentblock=blockafterrotate
```
定义land函数来使俄罗斯方块着陆。
```python
def land(event):
    global currentblock
    if currentblock is None:
        return

    cell_list=currentblock['cell_list']
    cc,cr=currentblock['cr']
    min_height=Row
    for cell in cell_list:
        cell_c,cell_r=cell
        c,r=cell_c+cc,cell_r+cr
        if r>=0 and block_list[r][c]:
            return
        h=0
        for i in range(r+1,Row):
            if block_list[i][c]:
                break
            else:
                h +=1
        if h<min_height:
            min_height=h

    down=[0,min_height]
    if checkmove(currentblock,down):
        draw_blockmoving(canvas,currentblock,down)
```
分别绑定键盘上的上下左右键。
```python
canvas.focus_set()  #聚焦到canvas画板对象
canvas.bind("<Left>",horizontalmoveblock)
canvas.bind("<Right>",horizontalmoveblock)
canvas.bind("<Up>",rotate)
canvas.bind("<Down>",land)
```
在所有方块都基本设定后，最后实现方块的消除与得分。定义checkrow函数判断指定行是否可以消除。
```python
def checkrow(row):
    for i in row:
        if i=='':
            return False
    return True
```
同时定义checkandclear函数检查所有行并消除。
```python
def checkandclear():
    completed_row=False
    for i in range(len(block_list)):
        if checkrow(block_list[i]):
            completed_row=True  #当前行可消除
            if i>0:
                for current_i in range(i,0,-1):
                    block_list[current_i]=block_list[current_i-1][:]
                block_list[0]=[''for j in range(Column)]
            else:
                block_list[i]=['' for j in range(Column)]
            global score
            score +=10

    if completed_row:
        draw_board(canvas,block_list)
```
所有条件设置完毕后，在FPS后调用game_loop方法
```python
root.update()
root.after(FPS,game_loop)
```
程序运行
```python
root.mainloop()
 ```
## 效果展示
![image](https://github.com/wakaocs/tkinter/blob/2/tetris.png)