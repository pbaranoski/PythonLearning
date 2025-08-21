import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *
from tkinter.tix import *

import pandas as pd
import openpyxl as excel
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.styles import Fill, Color

import os


def getDirPath (lblLabel):
    dirPath = tk.filedialog.askdirectory()
    print("##Directory: "+dirPath)

    #entry2.insert(0,str(dirPath))
    lblLabel.config(text=dirPath)


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
    in_dir = lblSearchDirText.cget("text")

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


    ###########################################
    # Comparison has completed
    ###########################################
    #messagebox.showinfo("Complete", "Results have been generated!")


def main():

    ####################################################
    # define variables
    ####################################################
    global MDIWnd
    global lblSearchDirText
    global lblInFile2Text
    global lblOutFileText
    global txtSearchString

    ####################################################
    # Build window
    ####################################################
    MDIWnd= tk.Tk()
    MDIWnd.title("Find Search String")
    MDIWnd.geometry("1000x300")

    lblHdr = tk.Label(MDIWnd, text='Find Search String')
    lblHdr.config(font=('helvetica', 14))
    lblHdr.grid(row=0, column=3, columnspan=3, padx=5, pady=10)

    lblSpacer = tk.Label(MDIWnd, text="          ")
    lblSpacer.grid(row=0, column=0)

    ##############################
    # Select InFile1
    ##############################
    btnInFile1 = tk.Button(text='Select File', command=lambda:getDirPath(lblSearchDirText), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnInFile1.grid(row=1, column=1, padx=5, pady=3)

    #lblSearchDirLabel = tk.Label(MDIWnd, text='Input File 1:', bd=1, relief="sunken")
    lblSearchDirLabel = tk.Label(MDIWnd, text='Folder Path to Search:')
    lblSearchDirLabel.config(font=('helvetica', 10))
    lblSearchDirLabel.grid(row=1, column=2, sticky='e', pady=1)

    # Selected InFile1
    lblSearchDirText = tk.Label(MDIWnd, text="")
    lblSearchDirText.config(font=('helvetica', 10))
    lblSearchDirText.grid(row=1, column=3, sticky='w')


    ###############################
    # Columns to Omit
    ###############################
    lblSearchString = tk.Label(MDIWnd, text='Enter Search String:')
    lblSearchString.config(font=('helvetica', 10))
    lblSearchString.grid(row=4, column=2, sticky='e', pady=3)

    txtSearchString = tk.Entry (MDIWnd, width=90, justify="left") 
    txtSearchString.grid(row=4, column=3, sticky='w')

    ###############################
    # Buttons
    ###############################
    bthSearchFiles = tk.Button(text='Search Files', command=lambda:searchFiles(), bg='blue', fg='white', font=('helvetica',10, 'bold'))
    bthSearchFiles.grid(row=6, column=3, sticky='w', pady=10)

    ####################################
    # Process Window messages
    ####################################
    MDIWnd.mainloop()


if __name__ == "__main__":
    
    main()




