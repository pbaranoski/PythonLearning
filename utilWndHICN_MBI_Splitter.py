import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
#from tkinter.tix import *

import re

import os
import sys

cur_dir = ""


def get_txt_file(lblLabel):

    global cur_dir
    global sFileHeader
    global bChoicesLoaded

    filetypes = (
        ('txt files', '*.txt'),
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


def sel_txt_file(lblLabel):

    global cur_dir

    filetypes = (
        ('Text files', '*.txt'),
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
        filename = arrFileParts[0] + ".txt"
    elif arrFileParts[1].strip() != "txt":
        filename = arrFileParts[0] + ".txt"     

    # Assign selected filename to screen label
    lblLabel.config(text=filename)

    # set the current default directory for dialog box
    cur_dir = os.path.dirname(filename)
    print (cur_dir)


def initiateConvertNDCAction():

    global IN_HICN_MBI_txt
    global OUT_HICN_txt
    global OUT_MBI_txt

    ########################################
    # Perform validation of UI input fields
    ########################################

    # load variables with window values
    txtInFile1 = lblInFile1Text.cget("text")
    txtOutFile = lblOutFileText.cget("text")
    txtOutFile2 = lblOutFile2Text.cget("text")
  

    # Verify that input values have been entered/selected
    if txtInFile1 == "":
        messagebox.showerror("Error", "Input File 1 has not been selected!")
        return

    if txtOutFile == "":
        messagebox.showerror("Error", "HICN Output File has not been selected!")
        return

    if txtOutFile2 == "":
        messagebox.showerror("Error", "MBI Output File has not been selected!")
        return
    
    #####################################################
    # Assign filenames to global variables
    #####################################################
    IN_HICN_MBI_txt = txtInFile1
    OUT_HICN_txt = txtOutFile
    OUT_MBI_txt = txtOutFile2

    #####################################################
    # Build regular expressions for conversion
    #####################################################
    p_HICN = re.compile("^[0-9]{9}[A-Z]{1}[A-Z0-9]?$")

    ##################################
    # Open input file and process
    ##################################
    sNDC_11 = ""

    fHICN = open(OUT_HICN_txt,"w", encoding="ascii") 
    fMBI = open(OUT_MBI_txt,"w", encoding="ascii") 

    ##################################
    # Loop thru input file and process
    ##################################
    with open(IN_HICN_MBI_txt) as fi:
        for sInputRec in fi:

            sHICN_MBI = sInputRec.strip()

            if (p_HICN.match(sHICN_MBI)):
                # Write to HICN file
                fHICN.write(sHICN_MBI + "\n")    
            else:
                fMBI.write(sHICN_MBI + "\n")    


    # Close output files
    fHICN.close()
    fMBI.close()

    ###########################################
    # All NDCs in input file have been converted
    ###########################################
    messagebox.showinfo("Complete", "Results have been generated!")

    return 0


def main():

    ####################################################
    # define variables
    ####################################################
    global MDIWnd
    global lblInFile1Text
    global lblOutFileText
    global lblOutFile2Text
    global intChkbxIncludeDashes 

    ####################################################
    # Build window
    ####################################################
    MDIWnd= tk.Tk()
    MDIWnd.title("Split Finder Values into Separate HICN and MBI files")
    MDIWnd.geometry("1100x300")

    lblHdr = tk.Label(MDIWnd, text='Split Finder Values into Separate HICN and MBI files')
    lblHdr.config(font=('helvetica', 14))
    lblHdr.grid(row=0, column=3, columnspan=3, padx=5, pady=10)

    lblSpacer = tk.Label(MDIWnd, text="          ")
    lblSpacer.grid(row=0, column=0)

    ##############################
    # Select InFile1
    ##############################
    btnInFile1 = tk.Button(text='Select File', command=lambda:get_txt_file(lblInFile1Text), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnInFile1.grid(row=1, column=1, pady=3)

    #lblInFile1Label = tk.Label(MDIWnd, text='Input File 1:', bd=1, relief="sunken")
    lblInFile1Label = tk.Label(MDIWnd, text='Input File of Mixed HICNs and MBIs:')
    lblInFile1Label.config(font=('helvetica', 10))
    lblInFile1Label.grid(row=1, column=2, sticky='e', pady=1)

    # Selected InFile1
    lblInFile1Text = tk.Label(MDIWnd, text="")
    lblInFile1Text.config(font=('helvetica', 10))
    lblInFile1Text.grid(row=1, column=3, sticky='w')

    ###############################
    # Select HICN Output File 
    ###############################
    btnOutFile = tk.Button(text='Select File', command=lambda:sel_txt_file(lblOutFileText), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnOutFile.grid(row=3, column=1, padx=2, pady=3)

    lblOutFileLabel = tk.Label(MDIWnd, text='HICN Output File:')
    lblOutFileLabel.config(font=('helvetica', 10))
    lblOutFileLabel.grid(row=3, column=2, sticky='e')

    # Selected Output File
    lblOutFileText = tk.Label(MDIWnd, text='')
    lblOutFileText.config(font=('helvetica', 10))
    lblOutFileText.grid(row=3, column=3, sticky='w')

    ###############################
    # Select MBI Output File 
    ###############################
    btnOutFile2 = tk.Button(text='Select File', command=lambda:sel_txt_file(lblOutFile2Text), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnOutFile2.grid(row=4, column=1, padx=2, pady=3)

    lblOutFile2Label = tk.Label(MDIWnd, text='MBI Output File:')
    lblOutFile2Label.config(font=('helvetica', 10))
    lblOutFile2Label.grid(row=4, column=2, sticky='e')

    # Selected Output File
    lblOutFile2Text = tk.Label(MDIWnd, text='')
    lblOutFile2Text.config(font=('helvetica', 10))
    lblOutFile2Text.grid(row=4, column=3, sticky='w')

 
    ###############################
    # Buttons
    ###############################
    btnCompare = tk.Button(text='Create HICN and MBI Files', command=initiateConvertNDCAction, bg='blue', fg='white', font=('helvetica',10, 'bold'))
    btnCompare.grid(row=6, column=3, sticky='w', pady=10)

    ####################################
    # Process Window messages
    ####################################
    MDIWnd.mainloop()


if __name__ == "__main__":
    
    main()




