from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

###################
### 함수 선언부 ###
##################

## memory allocated and return list
def malloc(h,w):
    retMemory = []
    for _ in range(inH):
        tmpList = []
        for _ in range(inW):
            tmpList.append(0)
        retMemory.append(tmpList)
    return retMemory


#Image Loading Function
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname) #size of file (Byte)
    inH = inW = int(math.sqrt(fsize)) # essential code
    ## Memory allocate

    inImage = []
    inImage = malloc(inH, inW)
    # file --> memory

    with open(filename, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))
    print(inH, inW)
    print(inImage[98][97])
# Select File and load on memory Function
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent= window ,
                               filetypes = (("RAW File", "*.raw"),("All Files", "*.*")))
    loadImage(filename)
    equalImage()
def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    pass
def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    window.geometry(str(outH) + 'x' + str(outW))# 벽
    canvas = Canvas(window, height=outH, width=outW)# 보드
    paper = PhotoImage(height= outH, width = outW)# 빈 종이
    canvas.create_image((outH//2,outW//2), image= paper, state='normal')# 중앙에 고정
    ## 출력영상 --> 화면에 한점씩
    for i in range(outH):
        for k in range(outW):
            r = g = b= outImage[i][k]
            # pixel = outImage[i][k]
            paper.put("#%02x%02x%02x" % (r, g, b),(k, i))
    canvas.pack(expand=1, anchor=CENTER)
#####################################
##### 컴퓨터 비전(영상 처리) 알고리즘 함수 모음

# 동일 영상 알고리즘

def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    displayImage()


## 화소점 처리 알고리즘

def addImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    value = askinteger("밝게 하기", "밝게할 값", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (inImage[i][k] + value)
            if outImage[i][k] >= 255:
                outImage[i][k] = 255
    displayImage()
def subImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    value = askinteger("어둡게 하기", "어둡게할 값", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (inImage[i][k] - value)
            if outImage[i][k] <= 1:
                outImage[i][k] = 1
    displayImage()
def mulImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    value = askinteger("영상 곱셈", "곱할 값", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (inImage[i][k] * value)
            if outImage[i][k] >= 255:
                outImage[i][k] = 255
    displayImage()

def divImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    value = askinteger("밝게 하기", "밝게할 값", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (inImage[i][k] // value)
            if outImage[i][k] <= 255:
                outImage[i][k] = 0
    displayImage()

def reverseImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    # value = askinteger("밝게 하기", "밝게할 값", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (255-inImage[i][k])

    displayImage()
def binImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    # value = askinteger("이진화", "이진화", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > 127:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    displayImage()

def avgImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    # value = askinteger("이진화", "이진화", minvalue=1, maxvalue=255)
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum+= inImage[i][k]
        avg = sum/ (inH*inW)
    messagebox.showinfo("Average", avg)
    displayImage()

#파라볼라 알고리즘
def paraImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255- 255 * math.pow(input/128-1, 2))
    for i in range(inH):
        for k in range(inW):
            input = inImage[i][k]
            outImage[i][k] = LUT[inImage[i][k]]
    displayImage()






############기하학적 처리

def updownImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드, 출력 영상 크기 결정##
    outH = inH
    outW = inW
    ## Memory allocate
    outImage = []
    outImage = malloc(outH, outW)
    ## real Computer Vision algorithm
    for i in range(inH):
        for k in range(inW):
            outImage[inH-i-1][k] = inImage[i][k]
    displayImage()
######################
### 전역변수 선언부 ###
######################
inImage, outImage = [], [] ; inH, inW, outH, outW = [0]*4
window, canvas, paper = None, None, None
filename= ""


###################
### 메인 코드부 ###
###################
# 메인 코드  부분
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) ver 0.02")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게 하기", command=addImage)
comVisionMenu1.add_command(label="어둡게 하기", command=subImage)
comVisionMenu1.add_command(label="영상 곱셈", command=mulImage)
comVisionMenu1.add_command(label="영상 나눗셈", command=divImage)
comVisionMenu1.add_command(label="화소값 반전", command=reverseImage)
comVisionMenu1.add_command(label="이진화", command=binImage)
comVisionMenu1.add_command(label="입/출력 평균값", command=avgImage)
comVisionMenu1.add_command(label="파라볼라", command=paraImage)

comVisionMenu3=Menu(mainMenu)
mainMenu.add_cascade(label = "기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label= '상하반전', command = updownImage)


window.mainloop()
