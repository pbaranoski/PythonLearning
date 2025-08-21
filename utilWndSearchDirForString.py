import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter.tix import *

import os

#in_dir = r"C:\Users\user\Documents\PythonLearning"
#out_dir = r"C:\Users\user\Documents\PythonLearning"


def getDirPath ():
    dirPath = tk.filedialog.askdirectory()
    print("##Directory: "+dirPath)

    #entry2.insert(0,str(dirPath))
    lblFolderPathText.config(text=dirPath)

def openNewWindow():

    # Toplevel object which will
    # be treated as a new window
    ## This will hold content of Search Results
    newWindow = Toplevel(MDIWnd)
    # sets the title 
    newWindow.title("Search Results")
    # sets the geometry of toplevel
    newWindow.geometry("800x500") 

    global cTableContainer, fTable, sbHorizontalScrollBar, sbVerticalScrollBar 
    cTableContainer = tk.Canvas(newWindow)
    fTable = tk.Frame(cTableContainer)
    sbHorizontalScrollBar = tk.Scrollbar(newWindow)
    sbVerticalScrollBar = tk.Scrollbar(newWindow)

    createScrollableContainer() 
  
    return newWindow

def createScrollableContainer():

	cTableContainer.config(xscrollcommand=sbHorizontalScrollBar.set,yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
	sbHorizontalScrollBar.config(orient=tk.HORIZONTAL, command=cTableContainer.xview)
	sbVerticalScrollBar.config(orient=tk.VERTICAL, command=cTableContainer.yview)

	sbHorizontalScrollBar.pack(fill=tk.X, side=tk.BOTTOM, expand=tk.FALSE)
	sbVerticalScrollBar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
	cTableContainer.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.TRUE)
	cTableContainer.create_window(0, 0, window=fTable, anchor=tk.NW)

# Updates the scrollable region of the Canvas to encompass all the widgets in the Frame
def updateScrollRegion():
	cTableContainer.update_idletasks()
	cTableContainer.config(scrollregion=fTable.bbox())

def searchFiles():

    # load variables with window values
    strSearch = txtSearchString.get()
    in_dir = lblFolderPathText.cget("text")

    # Verify that input values have been entered/selected
    if in_dir == "":
        messagebox.showerror("Error", "No input directory has been selected!")
        return

    if strSearch == "":
        messagebox.showerror("Error", "No Search String has been entered!")
        return

    # Search for String
    sSearchResults = ""

    # Get list of files in selected directory
    fileList = (dirItem for dirItem in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir,dirItem)) )

    # Iterate thru files in directory
    for searchFile in fileList:
        #print (searchFile)
        idx = searchFile.find(".")
        extension = searchFile[idx:].lower()

        # only process text files
        if (extension == ".py" or extension == ".txt" or extension == ".sql"
         or extension == ".sh" ):
            #print(searchFile)
            pass
        else:
            # Skip file
            continue

        # Search file for search    
        inFile = os.path.join(in_dir,searchFile)
        
        with open(inFile,"r", errors="ignore") as inPYFile:
            inFilename = os.path.basename(inFile)
            #print(inFilename)
            in_recs = inPYFile.readlines()
            for in_rec in in_recs:
                fndIdx = in_rec.find(strSearch)
                if fndIdx >= 0:
                    result = inFilename + "-->" + in_rec + "\n"
                    sSearchResults += result

        # Close input file when done
        inPYFile.close()


    childWnd = openNewWindow()
    
    #Label(childWnd, text=sSearchResults, justify=LEFT).grid()
    Label(fTable, text=sSearchResults, justify=LEFT).grid()

    updateScrollRegion()

    #messagebox.showinfo("Complete", "Results have been generated!")
    #messagebox.showinfo("Complete", sSearchResults)


####################################################
# MAIN
####################################################
MDIWnd= tk.Tk()
MDIWnd.title("Search Window")

canvas1 = tk.Canvas(MDIWnd, width = 800, height = 300,  relief = 'raised')
canvas1.pack()

lblHdr = tk.Label(MDIWnd, text='Find Search String')
lblHdr.config(font=('helvetica', 18))
canvas1.create_window(350, 30, window=lblHdr)

# folder searching
lblFolderPathLabel = tk.Label(MDIWnd, text='Folder Path to Search:')
lblFolderPathLabel.config(font=('helvetica', 12))
canvas1.create_window(100, 70, window=lblFolderPathLabel)

# folder searching
lblFolderPathText = tk.Label(MDIWnd, text='')
lblFolderPathText.config(font=('helvetica', 12))
canvas1.create_window(330, 70, window=lblFolderPathText)

# Search string
lblSearchString = tk.Label(MDIWnd, text='Enter Search String:')
lblSearchString.config(font=('helvetica', 12))
canvas1.create_window(100, 120, window=lblSearchString)

# Text box
txtSearchString = tk.Entry (MDIWnd, width = 45) 
canvas1.create_window(330, 120, window=txtSearchString)

# Buttons
btnGetPath = tk.Button(text='Select Folder', command=getDirPath, bg='blue', fg='white', font=('helvetica',12, 'bold'))
canvas1.create_window(100, 220, window=btnGetPath)

btnSearch = tk.Button(text='Search Files', command=searchFiles, bg='blue', fg='white', font=('helvetica',12, 'bold'))
canvas1.create_window(250, 220, window=btnSearch)

#button1 = tk.Button(text='File Exists?', command=checkFile, bg='brown', fg='white', font=('helvetica',12, 'bold'))
#canvas1.create_window(300, 200, window=button1)

MDIWnd.mainloop()






