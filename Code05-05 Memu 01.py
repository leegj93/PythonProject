from tkinter import *
from tkinter import messagebox
def fileClick():
    messagebox.showinfo('Menu', 'Contents')

window =Tk()
mainMenu =Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label= 'File', menu = fileMenu) #click시 확장
fileMenu.add_command(label='Open', command= fileClick)
fileMenu.add_separator()
fileMenu.add_command(label='Close',  command=None)
window.mainloop()