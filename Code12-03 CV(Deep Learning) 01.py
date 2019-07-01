from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import time
import matplotlib.pyplot as plt
# 파일을 선택해서 메모리로 로딩하는 함수

####################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue=0) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory


# 파일을 메모리로 로딩하는 함수
def loadImageColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inImage = []
    photo = Image.open(fname) # PIL 객체
    inW = photo.width; inH=photo.height
    ## 메모리 확보
    for _ in range(3) :
        inImage.append(malloc(inH, inW))

    photoRGB = photo.convert('RGB')
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k,i))
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b

def openImageColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadImageColor(filename)
    equalImageColor()
    # histoImageColor(filename)

    displayImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    VIEW_X = outW;    VIEW_Y = outH;   step = 1

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, step) :
        tmpStr = ''
        for k in numpy.arange(0,outW, step) :
            i = int(i); k = int(k)
            r , g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def saveImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # if outImage == None :
    #     return
    # saveFp = asksaveasfile(parent=window, mode='wb',
    #                        defaultextension='*.jpg', filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))
    # if saveFp == '' or saveFp == None:
    #     return
    # outImage.save(saveFp.name)
    # print('Save~')

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def  equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i][k] = inImage[RGB][i][k]
    #############################
    displayImageColor()


def addImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                if inImage[RGB][i][k] + value > 255 :
                    outImage[RGB][i][k] = 255
                elif inImage[RGB][i][k] + value < 0 :
                    outImage[RGB][i][k] = 0
                else :
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value
    #############################
    displayImageColor()

def revImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 - inImage[RGB][i][k]
    #############################
    displayImageColor()

def paraImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###\
    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]
    #############################
    displayImageColor()

def morphImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2) # PIL 객체
    inW2 = photo2.width; inH2=photo2.height
    ## 메모리 확보
    for _ in range(3) :
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2) :
        for k in range(inW2) :
            r, g, b = photoRGB2.getpixel((k,i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):
            for RGB in range(3) :
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()


###########기하학적 처리

def  upDownImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;

    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
       for i in range(inH) :
           for k in range(inW) :
            outImage[RGB][inH-i-1][k] = inImage[RGB][i][k]

    displayImageColor()


# 영상 축소 알고리즘
def  zoomOutImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]

    displayImageColor()

# 영상 확대 알고리즘
def  zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i//scale][k//scale]

    displayImageColor()

def  rotateImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    for RGB in range(3):
        for i in range(inH) :
            for k in range(inW) :
                xs = i ; ys = k;
                xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
                yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
                if 0<= xd < inH and 0 <= yd < inW :
                    outImage[RGB][xd][yd] = inImage[RGB][i][k]

    displayImageColor()


def  histoImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inImage = []
    photo = Image.open(filename)  # PIL 객체
    r, g, b = photo.split()
    print(r.histogram())
    print(g.histogram())
    print(b.histogram())
    bins = list(range(256))
    plt.plot(bins, r.histogram(), 'r')
    plt.plot(bins, g.histogram(), 'g')
    plt.plot(bins, b.histogram(), 'b')
    plt.show()

def  histoImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    outCountList = [0] * 256
    normalCountList = [0] * 256
    # 빈도수 계산
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                outCountList[outImage[RGB][i][k]] += 1
        maxVal = max(outCountList); minVal = min(outCountList)
    High = 256
    # 정규화 = (카운트값 - 최소값) * High / (최대값 - 최소값)
    for i in range(len(outCountList)) :
        normalCountList[i] = (outCountList[i] - minVal) * High  / (maxVal-minVal)
    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)
    subWindow.geometry('256x256')
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256//2, 256//2), image=subPaper, state='normal')

    for i in range(len(normalCountList)) :
        for k in range(int(normalCountList[i])) :
            data= 0
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))
    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()


import numpy as np

def rgb2gray(rgb):

    r, g, b = rgb[0,:,:], rgb[1,:,:], rgb[2,:,:]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def  bwImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW


    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    ####### 진짜 컴퓨터 비전 알고리즘 #####
    # ## 영상의 평균 구하기.

    sum = []

    for RGB in range(3):
        sum.append(0)
        for i in range(inH):
            for k in range(inW):
                sum[RGB] += inImage[RGB][i][k]
    avg = [s // (inW * inH) for s in sum]

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] > avg[RGB]:
                    outImage[RGB][i][k] = 255
                else:
                    outImage[RGB][i][k] = 0

    displayImageColor()


def zoomOutImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH // scale;
    outW = inW // scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i // scale][k // scale] += inImage[RGB][i][k]
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] //= (scale * scale)

    displayImageColor()


# 영상 확대 알고리즘 (양선형 보간)
def zoomInImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH * scale;
    outW = inW * scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4  # 실수위치 및 정수위치
    x, y = 0, 0  # 실수와 정수의 차이값
    C1, C2, C3, C4 = [0] * 4  # 결정할 위치(N)의 상하좌우 픽셀
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                rH = i / scale;
                rW = k / scale
                iH = int(rH);
                iW = int(rW)
                x = rW - iW;
                y = rH - iH
                if 0 <= iH < inH - 1 and 0 <= iW < inW - 1:
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW + 1]
                    C3 = inImage[RGB][iH + 1][iW + 1]
                    C4 = inImage[RGB][iH + 1][iW]
                    newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                    outImage[RGB][i][k] = int(newValue)

    displayImageColor()


def zoomOutImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH // scale;
    outW = inW // scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i // scale][k // scale] += inImage[RGB][i][k]
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] //= (scale * scale)

    displayImageColor()


# 영상 확대 알고리즘 (양선형 보간)
def zoomInImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH * scale;
    outW = inW * scale;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    rH, rW, iH, iW = [0] * 4  # 실수위치 및 정수위치
    x, y = 0, 0  # 실수와 정수의 차이값
    C1, C2, C3, C4 = [0] * 4  # 결정할 위치(N)의 상하좌우 픽셀
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                rH = i / scale;
                rW = k / scale
                iH = int(rH);
                iW = int(rW)
                x = rW - iW;
                y = rH - iH
                if 0 <= iH < inH - 1 and 0 <= iW < inW - 1:
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW + 1]
                    C3 = inImage[RGB][iH + 1][iW + 1]
                    C4 = inImage[RGB][iH + 1][iW]
                    newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                    outImage[RGB][i][k] = int(newValue)

    displayImageColor()


def rotateImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW // 2;
    cy = inH // 2
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                xs = i;
                ys = k;
                xd = int(math.cos(radian) * (xs - cx) - math.sin(radian) * (ys - cy)) + cx
                yd = int(math.sin(radian) * (xs - cx) + math.cos(radian) * (ys - cy)) + cy
                if 0 <= xd < outH and 0 <= yd < outW:
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else:
                    outImage[RGB][xs][ys] = 255

    displayImageColor()


## 엠보싱 처리
def embossImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    MSIZE = 3
    mask = [[-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]]
    ## 임시 입력영상 메모리 확보
    tmpInImage = []
    tmpOutImage = []
    for _ in range(3):
        tmpInImage.append(malloc(inH + MSIZE - 1, inW + MSIZE - 1, 127))
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 --> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[RGB][i + MSIZE // 2][k + MSIZE // 2] = inImage[RGB][i][k]
        ## 회선연산
        for i in range(MSIZE // 2, inH + MSIZE // 2):
            for k in range(MSIZE // 2, inW + MSIZE // 2):
                # 각 점을 처리.
                S = 0.0
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSIZE // 2][k + n - MSIZE // 2]
                tmpOutImage[RGB][i - MSIZE // 2][k - MSIZE // 2] = S
        ## 127 더하기 (선택)
        for i in range(outH):
            for k in range(outW):
                tmpOutImage[RGB][i][k] += 127
        ## 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = int(value)

    displayImageColor()


####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2
inImage, outImage = [], []  # 3차원 리스트(배열)
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝) ver 0.01")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImagePIL)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImageColor)
comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2Color)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2Color)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImageColor)
comVisionMenu2.add_command(label="히스토그램2", command=histoImage2Color)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
# comVisionMenu3.add_command(label="이동", command=moveImage)
comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
comVisionMenu3.add_command(label="확대", command=zoomInImageColor)



window.mainloop()