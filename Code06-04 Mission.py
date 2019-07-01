from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

####################
#### 함수 선언부 ####
####################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(0)
        retMemory.append(tmpList)
    return retMemory


# 파일을 메모리로 로딩하는 함수
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드
    ## 입력영상 메모리 확보 ##
    inImage=[]
    inImage=malloc(inH,inW)
    # 파일 --> 메모리
    with open(filename, 'rb') as rFp:
        for i in range(inH) :
            for k in range(inW) :
                inImage[i][k] = int(ord(rFp.read(1)))

# 파일을 선택해서 메모리로 로딩하는 함수
def openImage() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    loadImage(filename)
    equalImage()

def saveImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    pass

def displayImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    ## 화면 크기를 조절
    window.geometry(str(outH) + 'x' + str(outW)) # 벽
    canvas = Canvas(window, height=outH, width=outW) # 보드
    paper = PhotoImage(height=outH, width=outW) # 빈 종이
    canvas.create_image((outH//2, outW//2), image=paper, state='normal')
    ## 출력영상 --> 화면에 한점씩 찍자.
    for i in range(outH) :
        for k in range(outW) :
            r = g = b = outImage[i][k]
            paper.put("#%02x%02x%02x" % (r, g, b), (k, i))

    canvas.pack(expand=1, anchor=CENTER)

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def  equalImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = inImage[i][k]

    displayImage()

# 동일영상 알고리즘
def  addImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    for i in range(inH) :
        for k in range(inW) :
            v = inImage[i][k] + value
            if v > 255 :
                v = 255
            elif v < 0 :
                v = 0
            outImage[i][k] = v

    displayImage()

# 반전영상 알고리즘
def  revImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()

# 이진화 알고리즘
def  bwImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    ## 영상의 평균 구하기.
    sum = 0
    for i in range(inH) :
        for k in range(inW) :
            sum += inImage[i][k]
    avg = sum // (inW * inH)

    for i in range(inH) :
        for k in range(inW) :
            if inImage[i][k] > avg :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0

    displayImage()

# 파라볼라 알고리즘 with LUT
def  paraImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    LUT = [0 for _ in range(256)]
    for input in range(256) :
        LUT[input]  = int(255 - 255 * math.pow(input/128 -1, 2))

    for i in range(inH) :
        for k in range(inW) :
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

def  right90rotateImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    for i in range(inH) :
        for k in range(inW) :
            outImage[k][inW-i-1] = inImage[i][k]

    displayImage()

def  moveImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    value1 = askinteger("상하", "값-->", minvalue=-255, maxvalue=255)
    value2 = askinteger("좌우", "값-->", minvalue=-255, maxvalue=255)
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    for i in range(inH) :
        for k in range(inW) :
            newY = i + value1
            newX = k + value2
            if newX <= 255 and newY <=255 and newX >= 0 and newY >= 0:
                outImage[newY][newX] = inImage[i][k]

    displayImage()

def  miniImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    value = askinteger("축소배율", "값(2 또는 4 입력)-->", minvalue=2, maxvalue=4)
    ###### 메모리 할당 ################
    outH = inH // value
    outW = inW // value
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####


    for i in range(outH) :
        for k in range(outW) :
            outImage[i][k] = inImage[i*value][k*value]

    displayImage()


def magnImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    value = askinteger("확대배율", "값(2의 배수)-->", minvalue=2)
    ###### 메모리 할당 ################
    outH = outH * value
    outW = outW * value
    outImage = [];
    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i//value][k//value]

    displayImage()
####################
#### 전역변수 선언부 ####
####################
inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
####################
#### 메인 코드부 ####
####################
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
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImage)
comVisionMenu1.add_command(label="반전하기", command=revImage)
comVisionMenu1.add_command(label="파라볼라", command=paraImage)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소(통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImage)

comVisionMenu3=Menu(mainMenu)
mainMenu.add_cascade(label = "기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label= '상하반전', command = updownImage)
comVisionMenu3.add_command(label= '오른쪽 90도 회전', command = right90rotateImage)
comVisionMenu3.add_command(label= '이동', command = moveImage)
comVisionMenu3.add_command(label= '축소', command = miniImage)
comVisionMenu3.add_command(label= '확대', command = magnImage)



window.mainloop()