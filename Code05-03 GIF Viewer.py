from tkinter import *
## 전역변수 선언부
dirName = "C:/Images\Pet_GIF/Pet_GIF(256x256)/"
fnameList = ["cat01_256.gif","cat02_256.gif","cat02_256.gif","cat03_256.gif","cat04_256.gif",
             "cat05_256.gif","cat06_256.gif"]
photoList = [None]* 6
num = 0

## 함수 선언부
def clickPrev() :
    global num
    num -= 1
    if num < 0:
        num = len(fnameList)
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName = pName


def clickNext() :
    global num
    num += 1
    if num >= len(fnameList) :
        num = 0
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image = photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName=pName

def HomePress(event):
    global num
    num = 0
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName = pName

def EndPress(event):
    global num
    num = len(fnameList)-1
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName = pName

def LeftPress(event):
    global num
    num -= 1
    if num < 0:
        num = len(fnameList)
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName = pName

def RightPress(event):
    global num
    num += 1
    if num >= len(fnameList):
        num = 0
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName = pName

def NumPress(event):
    global num
    num += int(event.char)
    if num >= len(fnameList):
        num = len(fnameList)-1
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    pName = fnameList[num]
    label1.configure(text=pName)
    label1.pName = pName




## 메인 코드부

window =Tk()
window.title('GIF PHOTO VIEWER Beta (Ver 0.01)')
window.geometry("500x300")
window.resizable(width=FALSE, height=TRUE)

photo = PhotoImage(file = dirName + fnameList[num])
pName = fnameList[num]
pLabel = Label(window, image=photo)
label1 = Label(window, text=pName)


btnPrev = Button(window, text = '<< 이전 그림', command = clickPrev )
btnNext = Button(window, text = '다음 그림 >> ', command = clickNext )

btnPrev.place(x=150, y=10)
btnNext.place(x= 350, y=10)
pLabel.place(x=15, y=50)
label1.place(x=250, y=10)

window.bind("<Home>", HomePress)
window.bind("<End>", EndPress)
window.bind("<Left>", LeftPress)
window.bind("<Right>", RightPress)
window.bind("<Key>", NumPress)

window.mainloop()