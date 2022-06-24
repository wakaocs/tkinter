from tkinter import Canvas, Label, Tk, messagebox
import random

Size=30
Row=20
Column=12
FPS=500
score=0

def draw_block(canvas,cc,rr,color="lightsteelblue"):
    x0=cc*Size
    y0=rr*Size
    x1=cc*Size+Size
    y1=rr*Size+Size
    canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline="white",width=2)

def draw_board(canvas,block_list):
    for i in range(Row):
        for j in range(Column):
            celltype=block_list[i][j]
            if celltype:
                draw_block(canvas,j,i,SHAPESCOLOR[celltype])
            else:
                draw_block(canvas,j,i)

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

def draw_shape(canvas,cc,rr,cell_list,color="lightsteelblue"):
    for i in cell_list:
        cell_c,cell_r=i
        col=cell_c+cc
        rol=cell_r+rr
        if 0<=cc<Column and 0<=rr<Row:
            draw_block(canvas,col,rol,color)

root=Tk()
root.title("俄罗斯方块")
root.geometry("800x600")
canvas=Canvas(root,width=360,height=600)
canvas.grid(row=0,column=0)
canvas1=Canvas(root,width=200,height=600)
canvas1.grid(row=1,column=1)
label=Label(root,text="键盘↑旋转方块\n\n键盘←向左移\n\n键盘→向右移\n\n键盘↓放置方块",font=("宋体",16))
label.place(x=500,y=200)

block_list=[]
for i in range(Row):
    irow=[''for j in range(Column)]
    block_list.append(irow)
draw_board(canvas,block_list)

def draw_blockmoving(canvas,block,direction=[0,0]):
    shapetype=block['kind']
    c,r=block['cr']
    cell_list=block['cell_list']
    draw_shape(canvas,c,r,cell_list)
    dc,dr=direction
    new_c,new_r=c+dc,r+dr
    block['cr']=[new_c,new_r]
    draw_shape(canvas,new_c,new_r,cell_list,SHAPESCOLOR[shapetype])

def generate_newblock():
    kind=random.choice(list(SHAPES.keys()))
    cr=[Column//2,0]
    newblock={
        'kind':kind,
        'cell_list':SHAPES[kind],
        'cr':cr
    }
    return newblock

def checkmove(block,direction=[0,0]):
    cc,cr=block['cr']
    cell_list=block['cell_list']
    for i in cell_list:
        cell_c,cell_r=i
        c=cell_c+cc+direction[0]
        r=cell_r+cr+direction[1]
        if c<0 or c>=Column or r>=Row:
            return False
        if r>=0 and block_list[r][c]:
            return False
    return True

def checkrow(row):
    for i in row:
        if i=='':
            return False
    return True

def checkandclear():
    completed_row=False
    for i in range(len(block_list)):
        if checkrow(block_list[i]):
            completed_row=True
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

def saveblocktolist(block):
    shapetype=block['kind']
    cc,cr=block['cr']
    cell_list=block['cell_list']
    for i in cell_list:
        cell_c,cell_r=i
        c=cell_c+cc
        r=cell_r+cr
        block_list[r][c]=shapetype

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
        draw_blockmoving(canvas,currentblock,direction)

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

def game_loop():
    root.update()
    global currentblock
    if currentblock is None:
        newblock=generate_newblock()
        draw_blockmoving(canvas,newblock)
        currentblock=newblock
        if not checkmove(currentblock,[0,0]):
            messagebox.showinfo("Game Over!","Your score is %s"%score)
            root.destroy()
            return
    else:
        if checkmove(currentblock,[0,1]):
            draw_blockmoving(canvas,currentblock,[0,1])
        else:
            saveblocktolist(currentblock)
            currentblock=None
            checkandclear()
    root.after(FPS,game_loop)

canvas.focus_set()
canvas.bind("<Left>",horizontalmoveblock)
canvas.bind("<Right>",horizontalmoveblock)
canvas.bind("<Up>",rotate)
canvas.bind("<Down>",land)
currentblock=None
root.update()
root.after(FPS,game_loop)
root.mainloop()