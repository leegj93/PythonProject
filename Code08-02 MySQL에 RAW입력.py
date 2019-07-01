from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import datetime

###################
### 전역 변수부 ###
###################
IP_ADDR = '192.168.56.107'; USER_NAME = 'root'; USER_PASSWORD = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET= 'utf8'
dfList=[]
g_avg=0
g_min=0
g_max=0


###################
### 함수부 ###
###################

def malloc(h, w, initValue=0):
    retMemory = []
    for _ in range(h):
        tmpList = []
        for _ in range(w):
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    global window, canvas, paper, dfList, inImage, outImage, inW, inH, outW, outH
    fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드 -> 정사각형이므로 루트를 씌우면 가로와 높이가 나옴.

    ## 입력영상 메모리 확보 ## - 512 x 512를 0으로 초기화 시킴.
    inImage = []  # load가 계속 될 수 있기 때문에 초기화 시키는 용도로 사용.
    inImage = malloc(inH,inW)
    # 파일 --> 메모리
    for i in range(len(dfList)):
        with open(dfList[i], 'rb') as rfp:  # 우리는 binary 이므로 rb 사용.(이미지이기 때문에 binary) cf. txt는 r
         for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rfp.read(1)))  # 1바이트만 읽는다.
    print(inH, inW)
    avgImage()
    # print(inImage[80][70])
def avgImage():
    global window, canvas, paper, dfList, inImage, outImage, inW, inH, outW, outH, g_avg, g_max, g_min
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    sum = 0
    min = 0
    max = 0
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] >= max:
                max = inImage[i][k]
                g_max= max
            elif inImage[i][k] <= min:
                min = inImage[i][k]
                g_min= min

            sum += inImage[i][k]
    avg = sum / (inH * inW)
    g_avg= avg
    # messagebox.showinfo("평균값은 얼마인가요?", avg)
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i][k] = int(avg)
    ## 한 사진에 똑같은 숫자들이 입력되면 한 색이 나온다.



def selectDirectory():
    dirList=[]

    dirName = askdirectory(parent= window)
    for dirName, subDirList, fnames in os.walk(dirName):
        for filename in fnames:
            if os.path.splitext(filename)[1].upper() == '.RAW':
                fileList= os.path.join(dirName, filename)
                dirList= dirName + '/' + filename
                dfList.append(dirList)
            if filename == '' or filename == None:
                return

            # edt1.insert(0, str(dirList))
    # print(dfList)
    # filename = askopenfilename(parent=window,
    #                            filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    # print(dfList)

def uploadData():
    con = pymysql.connect(host= IP_ADDR, user= USER_NAME, password= USER_PASSWORD, db=DB_NAME, charset = CHAR_SET)
    cur = con.cursor()


    fullname = edt1.get()
    for i in range(len(dfList)):
        dfList[i]
        with open(dfList[i], 'rb') as rfp:
            binData = rfp.read()
            loadImage(dfList[i])

        fname = os.path.basename(dfList[i])
        fsize = os.path.getsize(dfList[i])
        height = width = int(math.sqrt(fsize))
        now = datetime.datetime.now()
        upDate = now.strftime('%Y-%m-%d')
        upUser = USER_NAME
        raw_avg = g_avg
        raw_max = g_max
        raw_min = g_min
        sql = "INSERT INTO rawImage_TBL(raw_id, raw_Height, raw_Width, raw_fname, raw_update, raw_uploader, raw_avg, raw_max, raw_min, raw_data)"
        sql += "VALUES(NULL," + str(height) + "," + str(width) + ",'" + fname + "','"
        sql += upDate + "','" + upUser + "','" + str(raw_avg) + "','" + str(raw_max) + "','" + str(raw_min) + "', %s)"
        tupleData = (binData)
        cur.execute(sql, tupleData)

    con.commit()
    cur.close()
    con.close()



import tempfile
def downloadData():
    con = pymysql.connect(host= IP_ADDR, user= USER_NAME, password= USER_PASSWORD, db=DB_NAME, charset = CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()
    fullPath = tempfile.gettempdir() + '/' + fname
    with open(fullPath, 'wb') as wfp:
        wfp.write(binData)
    print(fullPath)
    cur.close()
    con.close()

###################
### 메인 코드부 ###
###################
# 메인 코드  부분
window = Tk()
window.geometry("500x200")
window.title("Raw --> DB Ver 0.02")

edt1 = Entry(window, width=50); edt1.pack()
btnFile = Button(window, text= "Select Folder", command= selectDirectory); btnFile.pack()
btnUpload = Button(window, text= "Upload Folder", command= uploadData); btnUpload.pack()
btndownload = Button(window, text= "DownLoad File", command= downloadData); btndownload.pack()



window.mainloop()
