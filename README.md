# 4*4格子
为了实现4*4格子，我使用canvas控件，再分别画5条竖线和5条横线。
因为一行一行输出
```python
canvas.create_line(30,30,30,150,width=2,fill='black') #第一条竖线
canvas.create_line(60,30,60,150,width=2,fill='black')  #第二条竖线
canvas.create_line(90,30,90,150,width=2,fill='black')  #第三条竖线
canvas.create_line(120,30,120,150,width=2,fill='black')  #第四条竖线
canvas.create_line(150,30,150,150,width=2,fill='black')  #第五条竖线
```
太麻烦，为了方便，我使用for循环
```python
for i in range(1,6):  
    canvas.create_line(i*30,30,i*30,150,width=2,fill='black')  
 ```
## 结果截图如下：
 ![image](https://github.com/wakaocs/tkinter/blob/main/2022-04-26%20(2).png)
