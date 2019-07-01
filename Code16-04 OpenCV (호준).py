from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np
import time
import csv
import cv2
import pymysql
####################
#### 함수 선언부 ####
####################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue=0, dataType=np.uint8) :
    retMemory = np.zeros((h,w),dtype=dataType)
    retMemory += initValue
    return retMemory

# 차원 변환
def dimTrans(ndarray,Height,Width):
    newArray=(ndarray.reshape(Height * Width, 3).T).reshape(3, Height, Width)
    return newArray


def saveTrans(ndarray,Height,Width):
    newArray=ndarray.reshape(3, Width * Height)
    newArray=newArray.T
    newArray=newArray.reshape(Height,Width, 3)
    return newArray


# 파일을 메모리로 로딩하는 함수
def loadImageColor(fname_CVdata) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    inImage = []
    ######################################
    # PIL 개체 -> OpenCV 개체로 복사
    if type(fname_CVdata) == str : # 문자열 = 파일name으로 넘어온것
        cvData = cv2.imread(fname_CVdata) # 파일 ->   CV데이터
    else:
        cvData = fname_CVdata # 데이터로 취급

    cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB)
    photo = Image.fromarray(cvPhoto)
    inH, inW, channels = cvPhoto.shape
    inImage = dimTrans(cvPhoto,inH,inW)



# 파일을 선택해서 메모리로 로딩하는 함수

def openImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    start = time.time()
    loadImageColor(filename)
    equalImageColor()
    displayImageColor()
    seconds = time.time() - start
    status.configure(text = status.cget("text") + "\t\t 시간(초):" + "{0:.2f}".format(seconds))


def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    start = time.time()
    outArray = saveTrans(outImage, outH, outW)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    savePhoto.save(saveFp.name)
    seconds = time.time() - start
    status.configure(text=status.cget("text") + "\t\t 시간(초):" + "{0:.2f}".format(seconds))


def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    ## 고정된 화면 크기
    # 가로/세로 비율 계산
    ratio = outH / outW
    if outH <= VIEW_X :
        VIEW_X = outH; stepX = 1
    if outH > VIEW_X :
        if ratio < 1 :
            VIEW_X = int(512 * ratio)
        else :
            VIEW_X = 512
        stepX = outH / VIEW_X

    if outW <= VIEW_Y:
        VIEW_Y = outW; stepY = 1
    if outW > VIEW_Y:
        if ratio > 1 :
            VIEW_Y = int(512 * ratio)
        else :
            VIEW_Y = 512

        stepY = outW / VIEW_Y

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_X, width=VIEW_Y)
    paper = PhotoImage(height=VIEW_X, width=VIEW_Y)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, stepX) :
        tmpStr = ''
        for k in numpy.arange(0,outW, stepY) :
            i = int(i); k = int(k)
            r, g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)
    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def  equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    outImage = inImage[:]
    displayImageColor()

# 덧셈뺄셈 알고리즘
def  addImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    start = time.time()
    inImage = inImage.astype(np.int16) # 오버플로우 방지
    outImage = inImage + value

    # 조건으로 범위 지정

    outImage = np.where(outImage > 255, 255, outImage)
    outImage = np.where(outImage < 0, 0, outImage)
    outImage = outImage.astype(np.uint8)

    displayImageColor()

# 반전영상 알고리즘
def  revImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    inImage = inImage.astype(np.int16)
    outImage = 255 - inImage
    outImage = outImage.astype(np.uint8)
    displayImageColor()

# 이진화 알고리즘
def  bwImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    # avg = np.mean(inImage)

    inImage = inImage.astype(np.int16)

    outImage = inImage

    # greyscale으로 변환
    # 메모리 확보
    grey =[]
    for _ in range(3):
        grey.append(malloc(inH,inW))
    # greyscale
    for RGB in range(3):
        grey[RGB] = (inImage[R]+inImage[G]+inImage[B])//3
    # 평균
    avg = np.mean(grey).astype(np.int16)

    # 이진화
    outImage = np.where(grey > avg, 255, outImage)
    outImage = np.where(grey < avg, 0, outImage)

    outImage = outImage.astype(np.uint8)

    displayImageColor()

# 파라볼라 알고리즘 with LUT
def paraImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = inImage[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    x = np.array([i for i in range(0, 256)])
    LUT = 255 - 255*np.power(x/128 - 1, 2)
    LUT = LUT.astype(np.uint8)
    outImage = LUT[inImage]
    displayImageColor()

def morphImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2)
    inW2 = photo2.width;
    inH2 = photo2.height
    ###### 메모리 할당 ################
    outImage = inImage[:]
    temp2 = np.array(photo2).ravel()
    inImage2 = np.vstack((temp2[::3], temp2[1::3], temp2[2::3])).reshape(3, inH2, inW2)

    ## 컴퓨터비전 알고리즘 ##
    import threading
    import time
    def morpFunc(): # scope 문제 주의 !!
        global outImage
        w1 = 1;
        w2 = 0
        for _ in range(20):
            newValue = inImage*w1 + inImage2*w2
            newValue = np.where(newValue > 255, 255, newValue).astype(np.uint8)
            outImage = newValue # 지역변수 취급되므로 global로 잡아야함
            displayImageColor()
            w1 -= 0.05;
            w2 += 0.05
            time.sleep(0.5)
    threading.Thread(target=morpFunc).start()

def addSValuePillow():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo
    ## 중요! 출력영상 크기 결정 ##
    value = askfloat("","연하게0~1, 진하게1~10")
    photo2 = photo.copy()
    photo2 =ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value)
    ###### 메모리 할당 ################
    outImage = dimTrans(np.array(photo2),outH,outW)

    displayImageColor()

# 상하반전
def upDownImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = inImage[:]
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    outImage = inImage[::-1, :]
    displayImageColor()

# 화면이동 알고리즘
def moveImageColor() :
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')

def mouseClick(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx,sy,ex,ey, panYN
    if panYN == False :
        return
    sx = event.x; sy = event.y

def mouseDrop(event) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global sx, sy, ex, ey, panYN
    if panYN == False :
        return
    ex = event.x;    ey = event.y
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = []
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    start = time.time()

    mx = ex - sx; my = ey - sy

    inImage = inImage.astype(np.int16)

    if mx > 0 and my > 0:
        outImage[:,my:outH,mx:outW] = inImage[:,0:inH-my,0:inW-mx]
    elif mx > 0 and my <0:
        outImage[:,0:outH + my, mx:outW] = inImage[:,-1*(my):inH, 0:inW - mx]
    elif mx < 0 and my > 0:
        outImage[:,my:outH,0:outW+mx] = inImage[:,0:inH-my,-1*(mx):inW]
    elif mx < 0 and my < 0:
        outImage[:,0:outH+my,0:outW+mx] = inImage[:,-1*(my):inH,-1*(mx):inW]

    outImage = outImage.astype(np.uint8)

    panYN = False
    print("걸린시간:", time.time() - start)
    displayImageColor()

# 축소
def zoomOutImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    inImage = inImage.astype(np.int16)

    outImage = inImage[::scale,::scale]

    outImage = outImage.astype(np.uint8)

    displayImageColor()

# 확대
def  zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    inImage = inImage.astype(np.int16)

    outImage = np.kron(inImage, np.ones((scale,scale)))

    outImage = outImage.astype(np.uint8)

    displayImageColor()

import matplotlib.pyplot as plt
def histoImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    hist, bins = np.histogram(outImage.ravel(), 256, [0, 256])
    histR, bins = np.histogram(outImage[R].ravel(), 256, [0, 256])
    histG, bins = np.histogram(outImage[G].ravel(), 256, [0, 256])
    histB, bins = np.histogram(outImage[B].ravel(), 256, [0, 256])


    plt.plot(histR, color="red")
    plt.plot(histG, color="green")
    plt.plot(histB, color="blue")
    plt.plot(hist, color="black")
    plt.show()

def histoImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW

    # 전체
    histAll, bins = np.histogram(outImage.ravel(), 256,[0,256])

    maxVal = np.max(histAll)
    minVal = np.min(histAll)
    High = 256

    normalCountList = np.array((histAll - minVal) * High  / (maxVal-minVal))

    # Red
    histR, bins = np.histogram(outImage[R].ravel(),256,[0,256])

    maxVal_R = np.max(histR)
    minVal_R = np.min(histR)

    normalCountList_R = np.array((histR - minVal_R) * High / (maxVal_R - minVal_R))

    # Green
    histG, bins = np.histogram(outImage[G].ravel(), 256, [0, 256])

    maxVal_G = np.max(histG)
    minVal_G = np.min(histG)

    normalCountList_G = np.array((histG - minVal_G) * High / (maxVal_G - minVal_G))

    # Blue
    histB, bins = np.histogram(outImage[B].ravel(), 256, [0, 256])

    maxVal_B = np.max(histB)
    minVal_B = np.min(histB)

    normalCountList_B = np.array((histB - minVal_B) * High / (maxVal_B - minVal_B))


    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)
    subWindow.geometry('256x256')
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256//2, 256//2), image=subPaper, state='normal')

    for i in range(len(normalCountList_R)) :
        for k in range(int(normalCountList_R[i])) :
            data= 100
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))

    for i in range(len(normalCountList_G)) :
        for k in range(int(normalCountList_G[i])) :
            data= 150
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))

    for i in range(len(normalCountList_B)) :
        for k in range(int(normalCountList_B[i])) :
            data= 200
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))

    for i in range(len(normalCountList)) :
        for k in range(int(normalCountList[i])) :
            data= 0
            subPaper.put('#%02x%02x%02x' % (data, data, data), (i, 255-k))

    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()

# stretch
def stretchImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    inImage = inImage.astype(np.int16)

    minVal = [np.min(inImage[R]), np.min(inImage[G]), np.min(inImage[B])]
    maxVal = [np.max(inImage[R]), np.max(inImage[G]), np.max(inImage[B])]

    for RGB in range(3):
        outImage[RGB]=((inImage[RGB] - minVal[RGB]) / (maxVal[RGB] - minVal[RGB])) * 255

    outImage = np.array(outImage).astype(np.uint8)

    displayImageColor()

# 평활화
def equalizeImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    ## 히스토그램

    hist, bins = np.histogram(inImage.ravel(), 256,[0,256]) # bins = 빈도수
    cdf = hist.cumsum() # 누적합
    cdf_m = np.ma.masked_equal(cdf, 0) # cdf에서 값이 0인 것은 mask 처리하며 계산에서 제외됨
    # History Equalization 공식
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    # Mask처리를 했던 부분을 다시 0으로 변환
    cdf = np.ma.filled(cdf_m, 0).astype(np.uint8)
    outImage = cdf[inImage]

    displayImageColor()


def loadCsvColor(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # 입력 영상 메모리 확보
    tempImage = np.loadtxt(fname, delimiter=",", dtype=np.int16)
    inH = tempImage[-1][0] + 1
    inW = tempImage[-1][1] + 1
    inImage = np.vstack((tempImage[:, 2],tempImage[:, 3],tempImage[:, 4])).reshape(3,inH,inW)

def openCsvColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH,outW
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == "" or filename == None:
        return
    loadCsvColor(filename)
    equalImageColor()


# 임시 경로에 outImage를 저장하기
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + os.path.basename(filename)
    if saveFp == "" or saveFp == None:
        return
    saveFp = open(saveFp, mode="wb")
    outArray = saveTrans(outImage, outH, outW)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), "RGB")

    savePhoto.save(saveFp.name)
    saveFp.close()

    return saveFp

def saveCsvColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension="*.csv", filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    with open(saveFp.name, mode="w", newline="") as wFp:
        csvWriter = csv.writer(wFp)
        for i in range (outH):
            for k in range (outW):
                row_list = [i, k, outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]]
                csvWriter.writerow(row_list)

def saveMySQLColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try:
        sql = "CREATE TABLE colorImage_TBL (raw_id INT AUTO_INCREMENT PRIMARY KEY, raw_fname VARCHAR(30), raw_extname CHAR(5), raw_height SMALLINT, raw_width SMALLINT, raw_data LONGBLOB);"
        cur.execute(sql)

    except:
        pass

    # outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달
    fullname = saveTempImage()
    fullname = fullname.name

    with open(fullname, "rb") as rfp:    # rb = read binary
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    height = outH
    width = outW

    sql = "INSERT INTO colorimage_tbl (raw_id, raw_fname, raw_extname, raw_height, raw_width, raw_data)"
    sql += " VALUES(NULL, '" + fname + "', '" + extname + "', " + str(height) + ", " + str(width) + ", %s)"

    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    # os.remove(fullname)

    print("끝!!")

# MySQL에서 불러오기

def loadMySQLColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PW, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width FROM colorimage_tbl"
    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [":".join(map(str,row)) for row in queryList]

    def selectRecord():
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]
        subWindow.destroy()
        raw_id = queryList[selIndex][0]
        sql = "SELECT raw_fname, raw_extname, raw_data FROM colorimage_tbl WHERE raw_id = " + str(raw_id)
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()
        import tempfile

        # 모든 windows 컴퓨터에 있는 temp 폴더에 저장하기
        fullPath = tempfile.gettempdir() + "/" + fname + "." + extname
        with open(fullPath, "wb") as wfp:  # wb = write binary
            wfp.write(binData)
        cur.close()
        con.close()

        loadImageColor(fullPath)
        equalImageColor()
        os.remove(fullPath)

    # 서브 윈도우에 목록 출력하기
    subWindow = Toplevel(window)    # Toplevel(window) = "window라는 Tk 밑에 있는 새로운 Tk이다"라는 뜻

    # subWindow.geometry("256x256")
    listbox = Listbox(subWindow)
    button = Button(subWindow, text="선택", command = selectRecord)
    for rowStr in rowList:
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    subWindow.mainloop()

    cur.close()
    con.close()

################################################
# OpenCV용 컴퓨터 딥러닝
###############################################
def toColorOutArray(pillowPhoto):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ###### 메모리 할당 ################
    outH = pillowPhoto.height
    outW = pillowPhoto.width
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    photoRGB = pillowPhoto.convert("RGB")
    outImage= dimTrans(np.array(photoRGB), outH, outW)
    displayImageColor()

def greydisplay():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy()

    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X

    window.geometry(str(int(VIEW_Y * 1.2)) + 'x' + str(int(VIEW_X * 1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')

    rgbStr = ''  # 전체 픽셀의 문자열을 저장
    for i in np.arange(0, outH, step):
        tmpStr = ''
        for k in np.arange(0, outW, step):
            i = int(i);
            k = int(k)
            r = g = b = outImage[i][k]
            tmpStr += ' #%02x%02x%02x' % (r, g, b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def embossOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ##### 알고리즘 #####
    mSize = askinteger("홀수값을 입력하시오", "마스크 크기")
    mask = np.zeros((mSize,mSize), np.float32)
    mask[0][0] = -1
    mask[mSize-1][mSize-1] = 1
    cvPhoto2 = cv2.filter2D(cvPhoto, -1, mask)
    cvPhoto2 += 127

    outImage=dimTrans(cvPhoto2,outH,outW)

    displayImageColor()

def greyScaleOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto

    ##### 알고리즘 #####
    outImage = cv2.cvtColor(cvPhoto, cv2.COLOR_RGB2GRAY)
    print(outImage.shape)
    greydisplay()

def blurOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ##### 알고리즘 #####
    mSize = askinteger("홀수값을 입력하시오", "마스크 크기")
    mask = np.ones((mSize,mSize), np.float32) / (mSize*mSize)
    cvPhoto2 = cv2.filter2D(cvPhoto, -1, mask)

    outImage = dimTrans(cvPhoto2, outH, outW)

    displayImageColor()

def rotateOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ##### 알고리즘 #####
    cvPhoto2 = cvPhoto[:]

    angle = askinteger("회전", "각도")
    rotate_matrix = cv2.getRotationMatrix2D((outH//2,outW//2), angle, 1) # 중앙점, 각도, scale(확대옵션)
    cvPhoto2 = cv2.warpAffine(cvPhoto, rotate_matrix, (outH, outW))

    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArray(photo2)

    # outImage = dimTrans(cvPhoto2, outH, outW)

    # displayImageColor()

def zoomOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ##### 알고리즘 #####
    scale = askfloat("배율", "배율를 입력하시오")
    cvPhoto2 = cv2.resize(cvPhoto, None, fx=scale, fy=scale)

    outImage = dimTrans(cvPhoto2, int(inH*scale), int(inW*scale))

    channels, outH, outW = outImage.shape

    displayImageColor()

def waveHorOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ##### 알고리즘 #####
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            oy = int(15.0 * math.sin(2*3.14*k/180))
            ox = 0
            if i+oy <inH:
                cvPhoto2[i][k] = cvPhoto[(i+oy)%inH][k]
            else:
                cvPhoto2[i][k]

    outImage = dimTrans(cvPhoto2, outH, outW)

    displayImageColor()

def waveVirOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ##### 알고리즘 #####
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            ox = int(25.0 * math.sin(2*3.14*i/180))
            oy = 0
            if k+ox <inW:
                cvPhoto2[i][k] = cvPhoto[i][(k+ox)%inW]
            else:
                cvPhoto2[i][k]
    outImage = dimTrans(cvPhoto2, outH, outW)

    displayImageColor()

def cartoonOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto

    ##### 알고리즘 #####
    baseColor = cv2.bilateralFilter(cvPhoto,15,125,75)
    baseGrey = cv2.cvtColor(cvPhoto, cv2.COLOR_RGB2GRAY)
    baseGrey = cv2.medianBlur(baseGrey, 11)
    edges = cv2.Laplacian(baseGrey, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    baseEdge = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    rawBase = np.ma.masked_equal(baseColor*baseEdge,255)
    cvPhoto2 = baseEdge - rawBase

    outImage = dimTrans(cvPhoto2, outH, outW)

    displayImageColor()

def denoiseOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto

    ##### 알고리즘 #####
    cvPhoto2 = cv2.bilateralFilter(cvPhoto,15,125,75)

    outImage=dimTrans(cvPhoto2,outH,outW)
    displayImageColor()

################ 머신러닝 ####################
def faceDetectOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    print(face_rects)
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    ###################################################
    outImage = dimTrans(cvPhoto2, outH, outW)
    displayImageColor()

def hanibalOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:/images/images(ML)/mask_hannibal.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    grey = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴 찾기
    face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in face_rects:
        if h> 0 and w > 0 :
            x = int(x + 0.1*w); y = int(y+0.4*h)
            w = int(0.8 *w) ; h = int(0.8*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w]
            faceMask_small = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA)
            grey_mask = cv2.cvtColor(faceMask_small, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(grey_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_small, faceMask_small, mask=mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2,mask_inv)
            cvPhoto2[y:y+h, x:x+w] = cv2.add(maskedFace, maskedFrame)
    ###################################################
    outImage = dimTrans(cvPhoto2, outH, outW)
    displayImageColor()

def sunglassOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ###이 부분이 OpenCV 처리 부분##########################
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')

    if face_cascade.empty():
        raise IOError('Unable to load the face cascade classifier xml file')
    if eye_cascade.empty():
        raise IOError('Unable to load the eye cascade classifier xml file')

    cvPhoto2 = cvPhoto[:]
    sunglasses_img = cv2.imread('C:/images/images(ML)/eye_sunglasses_1.jpg')

    img = cvPhoto2

    gray = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    centers = []
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (x_eye, y_eye, w_eye, h_eye) in eyes:
            cv2.rectangle(roi_color, (x_eye,y_eye), (x_eye+w_eye,y_eye+h_eye), (0,255,0), 3)
            centers.append((x + int(x_eye + 0.5 * w_eye), y + int(y_eye + 0.5 * h_eye)))

    if len(centers) > 0:
        # Overlay sunglasses
        sunglasses_width = 2.12 * abs(centers[1][0] - centers[0][0])
        overlay_img = np.ones(img.shape, np.uint8) * 255
        h, w = sunglasses_img.shape[:2]
        scaling_factor = sunglasses_width / w
        overlay_sunglasses = cv2.resize(sunglasses_img, None, fx=scaling_factor,
                                        fy=scaling_factor, interpolation=cv2.INTER_AREA)

        x = centers[0][0] if centers[0][0] < centers[1][0] else centers[1][0]
        x -= int(0.26 * overlay_sunglasses.shape[1])
        y += int(0.85 * overlay_sunglasses.shape[0])
        h, w = overlay_sunglasses.shape[:2]
        overlay_img[y:y + h, x:x + w] = overlay_sunglasses

        # Create mask
        gray_sunglasses = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_sunglasses, 110, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        temp = cv2.bitwise_and(img, img, mask=mask)
        temp2 = cv2.bitwise_and(overlay_img, overlay_img, mask=mask_inv)
        mid_img = cv2.add(temp, temp2)
        final_img = cv2.cvtColor(mid_img, cv2.COLOR_BGR2RGB)

        # cv2.imshow('Eye Detector', img)
        cv2.imshow('Sunglasses', final_img)
        cv2.waitKey()
        cv2.destroyAllWindows()


################ 딥러닝 #####################

def deepOpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
      ###########################
    CONF_VALUE = 0.2
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
    image = cvPhoto
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    cvPhoto2 = image
    ############################
    outImage = dimTrans(cvPhoto2,h,w)
    displayImageColor()

def deepEqualizeImageColor(frame) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH, outW, channels = frame.shape
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####

    ## 히스토그램

    hist, bins = np.histogram(frame.ravel(), 256,[0,256]) # bins = 빈도수
    cdf = hist.cumsum() # 누적합
    cdf_m = np.ma.masked_equal(cdf, 0) # cdf에서 값이 0인 것은 mask 처리하며 계산에서 제외됨
    # History Equalization 공식
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    # Mask처리를 했던 부분을 다시 0으로 변환
    cdf = np.ma.filled(cdf_m, 0).astype(np.uint8)
    outImage = cdf[frame]

    return outImage

def deep2OpenCV() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    global frame
    filename = askopenfilename(parent=window,
             filetypes=(("동영상 파일", "*.mp4"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    cap = cv2.VideoCapture(filename)
    s_factor = 0.5 # 화면 크기 비율

    frameCount = 0


    while True :
        ret, frame = cap.read() # 현재 한 장면
        ret2, frameOut = cap.read()

        if not ret :
            break
        frameCount += 1
        if frameCount % 8 == 0 :  # 8은 화면 속도 조절
            frmH, frmW, channels = frame.shape
            frame = dimTrans(frame, frmH, frmW)
            frame = deepEqualizeImageColor(frame)
            frame = saveTrans(frame,frmH,frmW)
            frame = cv2.resize(frame, None, fx =s_factor, fy=s_factor,
                               interpolation=cv2.INTER_AREA)

            frameOut = cv2.resize(frameOut, None, fx=s_factor, fy=s_factor,
                               interpolation=cv2.INTER_AREA)

            ###########################
            CONF_VALUE = 0.2
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                "sofa", "train", "tvmonitor"]
            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
            net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
            image = frame

            imageOut = frameOut

            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > CONF_VALUE:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    cv2.rectangle(image, (startX, startY), (endX, endY),
                        COLORS[idx], 2)

                    cv2.rectangle(imageOut, (startX, startY), (endX, endY),
                                  COLORS[idx], 2)

                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                    cv2.putText(imageOut, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            frame = image

            # frameOut = imageOut

            ############################
            # cv2.imshow('Deep Learning', frame)

            cv2.imshow('Deep Learning', frameOut)

            c = cv2.waitKey(1)
            if c == 27 : # ESC키
                break
            elif c == ord('c') or c== ord('C') :
                captureVideo()
                window.update()

    cap.release()
    cv2.destroyAllWindows()

def captureVideo() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto, frame
    loadImageColor(frame)
    equalImageColor()

####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2
inImage, outImage = [], [] ; inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
panYN = False
sx,sy,ex,ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)

IP_ADDR = "192.168.56.112"
USER_NAME = "root"
USER_PW = "1234"
DB_NAME = "BigData_DB"
CHAR_SET = "utf8"


####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) ver 0.04")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트


mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImageColor)


comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_command(label="모핑", command=morphImageColor)
comVisionMenu1.add_command(label="채도조절(Pillow)", command=addSValuePillow)
# comVisionMenu1.add_command(label="채도조절(HSV)", command=addSValueHSV)



comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImageColor)
# comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2)
# comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2Color)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImageColor)
comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2Color)
comVisionMenu2.add_command(label="명암대비", command=stretchImageColor)
# comVisionMenu2.add_command(label="End-In탐색", command=endinImage)
comVisionMenu2.add_command(label="평활화", command=equalizeImageColor)
#
comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
# comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
comVisionMenu3.add_command(label="이동", command=moveImageColor)
comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
comVisionMenu3.add_command(label="확대", command=zoomInImageColor)
# comVisionMenu3.add_command(label="회전1", command=rotateImage)
# comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2Color)
#
comVisionMenu04 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu04)
# comVisionMenu04.add_command(label="엠보싱(RGB)", command=embossImageRGB)
# comVisionMenu04.add_command(label="엠보싱(HSV)", command=embossImageHSV)
# comVisionMenu04.add_command(label="엠보싱(PIL)", command=embossImagePIL)
# comVisionMenu04.add_command(label="블러링", command=blurImage)
# comVisionMenu04.add_command(label="샤프닝", command=sharpImage)
# comVisionMenu04.add_command(label="가우시안", command=gausImage)
# comVisionMenu04.add_command(label="고주파", command=hFreqImage)
# comVisionMenu04.add_command(label="저주파", command=lFreqImage)
# comVisionMenu04.add_separator()
# comVisionMenu04.add_command(label="경계선", command=dImage)
# comVisionMenu04.add_cascade(label="로버츠 행", command=d01Image)
# comVisionMenu04.add_cascade(label="프리윗 행", command=d02Image)
# comVisionMenu04.add_cascade(label="소벨 행", command=d03Image)
# comVisionMenu04.add_cascade(label="라플라시아b", command=d04Image)
# comVisionMenu04.add_cascade(label="라플라시아c", command=d05Image)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMySQLColor)
comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMySQLColor)
# comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCsvColor)
comVisionMenu5.add_command(label="CSV로 저장", command=saveCsvColor)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="Xls로 저장", command=saveExcel)
# comVisionMenu5.add_command(label="Xls Art로 저장", command=saveExcelArt)

openCVMEenu = Menu(mainMenu)
mainMenu.add_cascade(label="OpenCV 딥러닝", menu=openCVMEenu)
openCVMEenu.add_command(label="엠보싱(OpenCV)", command=embossOpenCV)
openCVMEenu.add_command(label="그레이스케일", command=greyScaleOpenCV)
openCVMEenu.add_command(label="블러링", command=blurOpenCV)
openCVMEenu.add_command(label="회전", command=rotateOpenCV) # 버그 O
openCVMEenu.add_command(label="확대 및 축소", command=zoomOpenCV)
openCVMEenu.add_command(label="수평웨이브", command=waveHorOpenCV)
openCVMEenu.add_command(label="수직웨이브", command=waveVirOpenCV)
openCVMEenu.add_command(label="카툰효과", command=cartoonOpenCV)
openCVMEenu.add_command(label="디노이즈", command=denoiseOpenCV)
openCVMEenu.add_separator()
openCVMEenu.add_command(label="얼굴인식 머신러닝", command=faceDetectOpenCV)
openCVMEenu.add_command(label="한니발 마스크", command=hanibalOpenCV)
openCVMEenu.add_command(label="선글라스", command=sunglassOpenCV)

openCVMEenu.add_separator()
openCVMEenu.add_command(label="사물 인식(정지영상)", command=deepOpenCV)
openCVMEenu.add_command(label="사물 인식(동영상)", command=deep2OpenCV) # 평활화버젼

window.mainloop()