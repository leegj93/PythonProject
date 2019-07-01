from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
import os

num = 0
TextList= [None]

fnameList = []

for dirName, subDirList, fnames in os.walk('c:/images/') :
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == '.TXT' :
            fullName = dirName + '/' + fname
            fnameList.append(fullName)



## Function

def selectFile() :
    outputTxt.delete(1.0, END)
    filename = askopenfilename(parent=window,
             filetypes=(("Text", "*.txt"),("All Files",'*.*')))
    print(filename)
    if filename == "":
        filename = None
    else:
        file = open(filename, "r")
        outputTxt.insert(1.0,file.read())
        file.close()

def saveFile() :
    filename = asksaveasfilename(parent=window,defaultextension=".txt",
             filetypes=(("Text", "*.txt"),("All Files",'*.*')))
    file = open(filename, "w")
    file.write(outputTxt.get(1.0, END))
    file.close()


    if filename == None:
        filename = asksaveasfilename(initialfile='Untitled.txt',
                                     defaultextension=".txt",
                                     filetypes=("Text", "*.txt"))
    else:
        file= open(filename, "w")
        file.write(outputTxt.get(1.0,END))
        file.close()
    print(filename)







## Window 구현
window =Tk()
window.title('Text File Viewer Beta (Ver 0.01)')
window.geometry("500x300")
window.resizable(width=FALSE, height=TRUE)
mainMenu =Menu(window)
window.config(menu=mainMenu)

mainFrame = Frame(window)
mainFrame.grid(column =0, row= 0)

## Txt 화면 출력

outputTxt= Text(mainFrame)

outputTxt.grid(column = 1, row= 1)






pText = Label(window)

#메뉴 [file]>> [open]

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label= 'File', menu = fileMenu) #click시 확장
fileMenu.add_command(label='Open', command=selectFile)

#메뉴 [file]>> [save]

fileMenu.add_command(label='Save', command=saveFile)


window.mainloop()



