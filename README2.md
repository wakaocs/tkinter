# 设计文档
## 程序实现说明及运行
要求：a)画16*16格子; b)界面有两个按钮,点其中一个按钮，格子点阵显示“交”字，点另一个按钮，格子点阵显示“大”字。
首先是格子，我使用canvas控件，再分别画5条竖线和5条横线。

先利用canvas函数画出16x16格子，思路：画一个大canvas,再分别画17条竖线及横线。
```python
from tkinter import BOTH,Tk,Canvas,Button
from tkinter.messagebox import YES
root = Tk()
root.title("画16*16格子")
root.geometry('600x600')
canvas=Canvas(root,background='white') #大画布
canvas.pack(expand=YES,fill=BOTH)
for i in range(1,18):  
    canvas.create_line(i*30,30,i*30,510,width=2,fill='black')  #竖线
for i in range(1,18):
    canvas.create_line(30,i*30,510,i*30,width=2,fill='black')  #横线
```
再来建立两个按钮，利用Button函数。
思路：为了在点击按钮时能显示文字，我定义了一个函数，之后在Button内的command再调用这函数。文字的显示则通过canvas内的控件create_text实现。
```python
def button_1(): #按钮一
  canvas.create_text(40,40,text="交")   
def button_2(): #按钮二
  canvas.create_text(140,140,text="大")  
btn1=Button(root,text="button1",width=10,command=button_1)
btn2=Button(root,text="button2",width=10,command=button_2)
btn1.pack()
btn2.pack() 
 ```
程序运行
```python
root.mainloop()
 ```
## 效果展示
https://github.com/wakaocs/tkinter/blob/main/wk2_Trim.mp4