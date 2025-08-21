import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
#from tkinter.tix import *

import pandas as pd
import openpyxl as excel
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.styles import Fill, Color

import os

import CompareTwoCSVFiles 

cur_dir = ""
sFileHeader = ""
bChoicesLoaded = False

sDropDownSelections = ""

#TBL_COLS1_csv = ""
#TBL_COLS2_csv = ""

###fDtlDiffs = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\PBAR\PBAR_IMPL\IMPL_CD_SGNTRS_Diffs.csv"
#fDtlDiffsXLSX = ""


def get_csv_file(lblLabel):

    global cur_dir
    global sFileHeader
    global bChoicesLoaded

    filetypes = (
        ('csv files', '*.csv'),
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=cur_dir,
        filetypes=filetypes 
    )

    # Verify filename has extension
    arrFileParts = os.path.splitext(filename)
    if arrFileParts[1].strip() == "":
        filename = arrFileParts[0] + ".csv"

    # Assign selected filename to screen label
    lblLabel.config(text=filename)

    # set the current default directory for dialog box
    cur_dir = os.path.dirname(filename)
    print (cur_dir)

    #################################################################
    # Read header record for file to get list of omit column choices
    #################################################################
    if bChoicesLoaded == False:
        bChoicesLoaded = True
        with open(filename, "r", encoding = 'utf-8') as f:
            sFileHeader = f.readline()
            print("header: "+sFileHeader)

        loadOmitChoices()    


def loadOmitChoices():

    # Create a Tkinter variable
    global tkDropdownSelection
    tkDropdownSelection = tk.StringVar(MDIWnd)

    # Dictionary with options
    lstOmitChoices = sFileHeader.split(",")
    tkDropdownSelection.set(lstOmitChoices[0]) # set the default option

    popupMenu = tk.OptionMenu(MDIWnd, tkDropdownSelection, *lstOmitChoices, command=dropdownSelectionMade)
    popupMenu.grid(row=4, column=4, pady=5)


def dropdownSelectionMade(choice):
    global sDropDownSelections

    choice = tkDropdownSelection.get()
    #print(f"choice:{choice}")

    # Get current textbox text 
    sDropDownSelections = txtOmitCols.get()

    # Add selection to textbox
    if sDropDownSelections == "":
        sDropDownSelections = choice
    else:     
        sDropDownSelections += ", " + choice 

    # modify text in textbox to include new selection
    txtOmitCols.delete(0, 'end')
    txtOmitCols.insert(0, sDropDownSelections)

    print(f"sDropDownSelections: {sDropDownSelections}")


def sel_xlsx_file(lblLabel):

    global cur_dir

    filetypes = (
        ('Excel files', '*.xlsx'),
    )

    filename = fd.asksaveasfilename(
        title='SaveAs file',
        initialdir=cur_dir,
        filetypes=filetypes 
    )

    # Verify filename has extension
    # and that extension is xlsx
    arrFileParts = os.path.splitext(filename)
    if arrFileParts[1].strip() == "":
        filename = arrFileParts[0] + ".xlsx"
    elif arrFileParts[1].strip() != "xlsx":
        filename = arrFileParts[0] + ".xlsx"     

    # Assign selected filename to screen label
    lblLabel.config(text=filename)

    # set the current default directory for dialog box
    cur_dir = os.path.dirname(filename)
    print (cur_dir)


def initiateCompareFilesAction():

    global TBL_COLS1_csv
    global TBL_COLS2_csv
    global fDtlDiffsXLSX
    global lstOmitColumns

    ########################################
    # 1) Perform validation of input fields
    # 2) Perform Compare
    ########################################

    # load variables with window values
    txtInFile1 = lblInFile1Text.cget("text")
    txtInFile2 = lblInFile2Text.cget("text")
    txtOutFile = lblOutFileText.cget("text")

    # Verify that input values have been entered/selected

    if txtInFile1 == "":
        messagebox.showerror("Error", "Input File 1 has not been selected!")
        return

    if txtInFile2 == "":
        messagebox.showerror("Error", "Input File 2 has not been selected!")
        return

    if txtOutFile == "":
        messagebox.showerror("Error", "Output File has not been selected!")
        return

    #####################################################
    # 1) Load variables needed by compareFiles function
    #    using screen input values.
    # 2) Perform csv file comparison
    #####################################################
    TBL_COLS1_csv = txtInFile1
    TBL_COLS2_csv = txtInFile2
    fDtlDiffsXLSX = txtOutFile
    sColumns = txtOmitCols.get().replace(" ","")
    sColumns = txtOmitCols.get().replace(",,",",")    

    lstOmitColumns = sColumns.split(",")
    for i in range(0,len(lstOmitColumns)):
        lstOmitColumns[i] = lstOmitColumns[i].strip()

    print(lstOmitColumns)

    #CompareTwoCSVFiles.compareFiles()
    
    ###########################################
    # Comparison has completed
    ###########################################
    messagebox.showinfo("Complete", "Results have been generated!")


def main():

    ####################################################
    # define variables
    ####################################################
    global MDIWnd
    global lblInFile1Text
    global lblInFile2Text
    global lblOutFileText
    global lblOmitCols
    global txtOmitCols

    ####################################################
    # Build window
    ####################################################
    MDIWnd= tk.Tk()
    MDIWnd.title("Compare Two CSV Files")
    MDIWnd.geometry("1000x300")

    lblHdr = tk.Label(MDIWnd, text='Compare Two CSV Files')
    lblHdr.config(font=('helvetica', 14))
    lblHdr.grid(row=0, column=3, columnspan=3, padx=5, pady=10)

    lblSpacer = tk.Label(MDIWnd, text="          ")
    lblSpacer.grid(row=0, column=0)

    ##############################
    # Select InFile1
    ##############################
    btnInFile1 = tk.Button(text='Select File', command=lambda:get_csv_file(lblInFile1Text), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnInFile1.grid(row=1, column=1, pady=3)

    #lblInFile1Label = tk.Label(MDIWnd, text='Input File 1:', bd=1, relief="sunken")
    lblInFile1Label = tk.Label(MDIWnd, text='Input File 1:')
    lblInFile1Label.config(font=('helvetica', 10))
    lblInFile1Label.grid(row=1, column=2, sticky='e', pady=1)

    # Selected InFile1
    lblInFile1Text = tk.Label(MDIWnd, text="")
    lblInFile1Text.config(font=('helvetica', 10))
    lblInFile1Text.grid(row=1, column=3, sticky='w')

    ###############################
    # Select InFile2
    ###############################
    btnInFile2 = tk.Button(text='Select File', command=lambda:get_csv_file(lblInFile2Text), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnInFile2.grid(row=2, column=1, pady=3)

    lblInFile2Label = tk.Label(MDIWnd, text='Input File 2:')
    lblInFile2Label.config(font=('helvetica', 10))
    lblInFile2Label.grid(row=2, column=2, sticky='e')

    lblInFile2Text = tk.Label(MDIWnd, text="")
    lblInFile2Text.config(font=('helvetica', 10))
    lblInFile2Text.grid(row=2, column=3, sticky='w')

    ###############################
    # Output File Label
    ###############################
    btnOutFile = tk.Button(text='Select File', command=lambda:sel_xlsx_file(lblOutFileText), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnOutFile.grid(row=3, column=1, padx=2, pady=3)

    lblOutFileLabel = tk.Label(MDIWnd, text='Output File:')
    lblOutFileLabel.config(font=('helvetica', 10))
    lblOutFileLabel.grid(row=3, column=2, sticky='e')

    # Selected Output File
    lblOutFileText = tk.Label(MDIWnd, text='')
    lblOutFileText.config(font=('helvetica', 10))
    lblOutFileText.grid(row=3, column=3, sticky='w')

    ###############################
    # Columns to Omit
    ###############################
    lblOmitCols = tk.Label(MDIWnd, text='Columns to Omit:')
    lblOmitCols.config(font=('helvetica', 10))
    lblOmitCols.grid(row=4, column=2, sticky='e', pady=3)

    txtOmitCols = tk.Entry (MDIWnd, width=90, justify="left") 
    txtOmitCols.grid(row=4, column=3, sticky='w')

    ###############################
    # Buttons
    ###############################
    btnCompare = tk.Button(text='Compare Files', command=initiateCompareFilesAction, bg='blue', fg='white', font=('helvetica',10, 'bold'))
    btnCompare.grid(row=6, column=3, sticky='w', pady=10)

    ####################################
    # Process Window messages
    ####################################
    MDIWnd.mainloop()


if __name__ == "__main__":
    
    main()




