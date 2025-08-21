import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox

import pandas as pd

import os

import convert_fw_to_csv 

cur_dir = ""
sFileHeader = ""
bChoicesLoaded = False

sDropDownSelections = ""



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


def get_txt_file(lblLabel):
    
    global cur_dir
    global sFileHeader
    global bChoicesLoaded

    filetypes = (
        ('txt files', '*.txt'),
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
        filename = arrFileParts[0] + ".txt"

    # Assign selected filename to screen label
    lblLabel.config(text=filename)

    # set the current default directory for dialog box
    cur_dir = os.path.dirname(filename)
    print (cur_dir)


def sel_csv_file(lblLabel):

    global cur_dir

    filetypes = (
        ('CSV files', '*.csv'),
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
        filename = arrFileParts[0] + ".csv"
    elif arrFileParts[1].strip() != "csv":
        filename = arrFileParts[0] + ".csv"     

    # Assign selected filename to screen label
    lblLabel.config(text=filename)

    # set the current default directory for dialog box
    cur_dir = os.path.dirname(filename)
    print (cur_dir)


def CreateCSVFilesAction():

    ########################################
    # 1) Perform validation of input fields
    # 2) Perform Compare
    ########################################

    # load variables with window values
    txtInFile1 = lblInFile1Text.cget("text")
    txtInFile2 = lblInFile2Text.cget("text")
    txtOutFile = lblOutFileText.cget("text")
    txtDelmtr = txtDelimiter.get()

    # Verify that input values have been entered/selected

    if txtDelmtr == "":
        messagebox.showerror("Error", "Delimiter is empty. Must enter a value.")
        return

    if len(txtDelmtr) > 1:
        messagebox.showerror("Error", "Delimiter can only be one byte.")
        return

    if txtInFile1 == "":
        messagebox.showerror("Error", "Source2Target mapping file has not been selected!")
        return

    if txtInFile2 == "":
        messagebox.showerror("Error", "Fixed-width input file has not been selected!")
        return

    if txtOutFile == "":
        messagebox.showerror("Error", "Output CSV file has not been selected!")
        return

    #####################################################
    # 1) Load variables needed by compareFiles function
    #    using screen input values.
    # 2) Perform csv file comparison
    #####################################################
    convert_fw_to_csv.Source2TargetCSV = txtInFile1
    convert_fw_to_csv.FBFile = txtInFile2
    convert_fw_to_csv.CSVFile = txtOutFile
    convert_fw_to_csv.txtDelimiter = txtDelmtr
 
    convert_fw_to_csv.createCSVFile()
    
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
    global txtDelimiter

    ####################################################
    # Build window
    ####################################################
    MDIWnd= tk.Tk()
    MDIWnd.title("Convert Fixed-width file to CSV File")
    MDIWnd.geometry("1000x300")

    lblHdr = tk.Label(MDIWnd, text='Convert Fixed-width file to CSV File')
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
    lblInFile1Label = tk.Label(MDIWnd, text='Source2Target Mapping File:')
    lblInFile1Label.config(font=('helvetica', 10))
    lblInFile1Label.grid(row=1, column=2, sticky='e', pady=1)

    # Selected InFile1
    lblInFile1Text = tk.Label(MDIWnd, text="")
    lblInFile1Text.config(font=('helvetica', 10))
    lblInFile1Text.grid(row=1, column=3, sticky='w')

    ###############################
    # Select InFile2
    ###############################
    btnInFile2 = tk.Button(text='Select File', command=lambda:get_txt_file(lblInFile2Text), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnInFile2.grid(row=2, column=1, pady=3)

    lblInFile2Label = tk.Label(MDIWnd, text='Fixed-width File:')
    lblInFile2Label.config(font=('helvetica', 10))
    lblInFile2Label.grid(row=2, column=2, sticky='e')

    lblInFile2Text = tk.Label(MDIWnd, text="")
    lblInFile2Text.config(font=('helvetica', 10))
    lblInFile2Text.grid(row=2, column=3, sticky='w')

    ###############################
    # Output File Label
    ###############################
    btnOutFile = tk.Button(text='Select File', command=lambda:sel_csv_file(lblOutFileText), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnOutFile.grid(row=3, column=1, padx=2, pady=3)

    lblOutFileLabel = tk.Label(MDIWnd, text='Output CSV File:')
    lblOutFileLabel.config(font=('helvetica', 10))
    lblOutFileLabel.grid(row=3, column=2, sticky='e')

    # Selected Output File
    lblOutFileText = tk.Label(MDIWnd, text='')
    lblOutFileText.config(font=('helvetica', 10))
    lblOutFileText.grid(row=3, column=3, sticky='w')

    ###############################
    # Delimiter override
    ###############################
    lblDelimiterLabel = tk.Label(MDIWnd, text='Delimiter')
    lblDelimiterLabel.config(font=('helvetica', 10))
    lblDelimiterLabel.grid(row=4, column=2, sticky='e')

    txtDelmtr = tk.StringVar()
    txtDelimiter = tk.Entry(textvariable=txtDelmtr,  font=('helvetica', 8, 'bold'), width=2 )
    txtDelimiter.grid(row=4, column=3, padx=2, pady=1, sticky="W" )
    txtDelimiter.insert(0, ",")

    ###############################
    # Buttons
    ###############################
    btnCompare = tk.Button(text='Create CSV File', command=CreateCSVFilesAction, bg='blue', fg='white', font=('helvetica',10, 'bold'))
    btnCompare.grid(row=6, column=3, sticky='w', pady=10)

    ####################################
    # Process Window messages
    ####################################
    MDIWnd.mainloop()


if __name__ == "__main__":
    
    main()




