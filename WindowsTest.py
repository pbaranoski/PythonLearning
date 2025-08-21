import tkinter as tk
from tkinter import filedialog
import os.path

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 600, height = 300,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Check if a File Exists')
label1.config(font=('helvetica', 18))
canvas1.create_window(300, 35, window=label1)

label2 = tk.Label(root, text='Enter File Path:')
label2.config(font=('helvetica', 12))
canvas1.create_window(300, 100, window=label2)

entry1 = tk.Entry (root, width = 90) 
canvas1.create_window(300, 140, window=entry1)

def checkFile ():
     
    file_exists = os.path.isfile(entry1.get())
    
    label3 = tk.Label(root, text=str(file_exists),font=('helvetica', 14, 'bold'))
    canvas1.create_window(300, 250, window=label3)

def getFile ():
    filename = tk.filedialog.askopenfilename(filetypes=[('all files', '.*'), ('text files', '.txt')])
    print("##Filename: "+filename)

    entry1.insert(0,str(filename))

button2 = tk.Button(text='Get File', command=getFile, bg='blue', fg='white', font=('helvetica',12, 'bold'))
canvas1.create_window(200, 200, window=button2)

button1 = tk.Button(text='File Exists?', command=checkFile, bg='brown', fg='white', font=('helvetica',12, 'bold'))
canvas1.create_window(300, 200, window=button1)

root.mainloop()