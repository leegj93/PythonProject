## 트리뷰 활용
from tkinter import *
from tkinter import  ttk
from tkinter.filedialog import *
import csv


window = Tk()
window.geometry('800x500')

def openCSV():
    global csvList
    filename = askopenfilename(parent=None,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    csvList = []
    sheet = ttk.Treeview(window)
    with open(filename)as rfp:
        reader = csv.reader(rfp)
        headerList = next(reader)  # 맨위의 행을 읽음
        sum = 0
        count = 0
        for cList in reader:
            csvList.append(cList)
        #기존 시트 클리어
    sheet.delete(*sheet.get_children())

    # 첫번째 열 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부이름
    sheet.heading('#0', text=headerList[0])
    # 두번째 이후 열 만들기

    sheet['columns'] = headerList[1:]  # 컬럼의 내부이름
    for colName in headerList[1:]:
        sheet.column(colName, width = 70)
        sheet.heading(colName, text=colName)

    for row in csvList:
        sheet.insert('', 'end',text=row[0], values =row[1:])
    sheet.pack(expand=1, anchor = CENTER)
    # sheet.column("A", width=70);
    # sheet.heading('A', text='제목2')
    # sheet.column("B", width=70);
    # sheet.heading('B', text='제목3')
    # sheet.column("C", width=70);
    # sheet.heading('C', text='제목4')

    # 내용 채우기
    # sheet.insert('', 'end', text='1열값1', values=('2열값1', '3열값1', '4열값1'))
    # sheet.insert('', 'end', text='1열값2', values=('2열값2', '3열값2', '4열값2'))
    # sheet.insert('', 'end', text='1열값3', values=('2열값3', '3열값3', '4열값3'))

    # sheet.pack()

import xlrd
def openExcel():
    global csvList
    filename = askopenfilename(parent=None,
                               filetypes=(("엑셀 파일", "*.xls;*.xlsx"), ("모든 파일", "*.*")))
    csvList = []
    sheet = ttk.Treeview(window)
    workbook = xlrd.open_workbook(filename)


    print(workbook.nsheets)
    wsList =workbook.sheets()
    headerList =[]
    for i in range(wsList[0].ncols):
        headerList.append(wsList[0].cell_value(0,i))

    for wsheet in wsList :
        rowCount = wsheet.nrows
        colCount = wsheet.ncols
        for i in range(1,rowCount):
            tmpList=[]
            for k in range(1, colCount):
                tmpList.append(wsheet.cell_value(i,k))
            csvList.append(tmpList)
        #기존 시트 클리어
    sheet.delete(*sheet.get_children())

    # 첫번째 열 만들기
    sheet.column('#0', width=70)  # 첫 컬럼의 내부이름
    sheet.heading('#0', text=headerList[0])
    # 두번째 이후 열 만들기

    sheet['columns'] = headerList[1:]  # 컬럼의 내부이름
    for colName in headerList[1:]:
        sheet.column(colName, width = 70)
        sheet.heading(colName, text=colName)

    # for row in csvList:
    #     sheet.insert('', 'end',text=row[0], values =row[1:])
    # sheet.pack(expand=1, anchor = CENTER)
    # sheet.column("A", width=70);
    # sheet.heading('A', text='제목2')
    # sheet.column("B", width=70);
    # sheet.heading('B', text='제목3')
    # sheet.column("C", width=70);
    # sheet.heading('C', text='제목4')

    # 내용 채우기
    # sheet.insert('', 'end', text='1열값1', values=('2열값1', '3열값1', '4열값1'))
    # sheet.insert('', 'end', text='1열값2', values=('2열값2', '3열값2', '4열값2'))
    # sheet.insert('', 'end', text='1열값3', values=('2열값3', '3열값3', '4열값3'))

    # sheet.pack()
mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Files", menu=fileMenu)
fileMenu.add_command(label="CSV 열기", command=openCSV)
fileMenu.add_command(label="Excel 열기", command=openExcel)

window.mainloop()