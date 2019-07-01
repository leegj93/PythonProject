from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *


def mouseClick(event):
    global x1, y1, x2, y2
    x1 = event.x
    y1 = event.y

def mouseDrop(event):
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    if penStyle == 'c':
        canvas.create_oval(x1, y1, x2, y2, width=penWidth, fill=penColor)
    elif penStyle == 'l':
        canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)


def getColor():
    global penColor
    color = askcolor()
    penColor = color[1]

def getWidth():
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요",
                          minvalue = 1, maxvalue = 10)

def clickCircle():
    global penStyle
    penStyle = 'c'


def clickLine():
    global penStyle
    penStyle = 'l'


## 전역 변수 선언 부분


window = None
canvas = None
x1,y1,x2,y2 = None, None, None, None
penColor = 'black'
penStyle = 'l'
penWidth = 5

## main

if __name__ == '__main__':
    window = Tk()
    window.title('그림판 비슷한 프로그램')
    canvas= Canvas(window, height= 300, width= 300)
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack()

    mainMenu = Menu(window)
    window.config(menu = mainMenu)
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = '설정', menu = fileMenu)
    fileMenu.add_command(label='선 색상 선택', command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label='선 두께 설정', command=getWidth)

    ShapeMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = '도형', menu= ShapeMenu)
    ShapeMenu.add_command(label='선', command = clickLine)
    ShapeMenu.add_command(label='원',command = clickCircle)

    window.mainloop()


