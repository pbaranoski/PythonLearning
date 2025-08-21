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

    global IN_NDC_txt
    global OUT_NDC_txt

    ########################################
    # Perform validation of UI input fields
    ########################################

    # load variables with window values
    txtInFile1 = lblInFile1Text.cget("text")
    txtOutFile = lblOutFileText.cget("text")

    # Verify that input values have been entered/selected
    if txtInFile1 == "":
        messagebox.showerror("Error", "Input File 1 has not been selected!")
        return

    if txtOutFile == "":
        messagebox.showerror("Error", "Output File has not been selected!")
        return

    #####################################################
    # Assign filenames to global variables
    #####################################################
    IN_NDC_txt = txtInFile1
    OUT_NDC_txt = txtOutFile

    #####################################################
    # Build regular expressions for conversion
    #####################################################
    #For a 10 digit NDC in the 4-4-2 format, add a 0 in the 1st position.
    #For a 10 digit NDC in the 5-3-2 format, add a 0 in the 6th position.
    #For a 10 digit NDC in the 5-4-1 format, add a 0 in the 10th position.
    #sNDC = "69639-103-01"  #69639-0103-01

    p_4_4_2 = re.compile("^[0-9]{4}-[0-9]{4}-[0-9]{2}$")
    p_5_3_2 = re.compile("^[0-9]{5}-[0-9]{3}-[0-9]{2}$")
    p_5_4_1 = re.compile("^[0-9]{5}-[0-9]{4}-[0-9]{1}$")

    p_5_4_2 = re.compile("^[0-9]{5}-[0-9]{4}-[0-9]{2}$")
    p_11 = re.compile("^[0-9]{11}$")

    ##################################
    # Open input file and process
    ##################################
    sNDC_11 = ""

    fo = open(OUT_NDC_txt,"w", encoding="ascii") 

    ##################################
    # Loop thru input file and process
    ##################################
    with open(IN_NDC_txt) as fi:
        for sInputRec in fi:

            sNDC = sInputRec.strip()

            if (p_4_4_2.match(sNDC)):
                sNDC_11 = '0' + sNDC
            elif (p_5_3_2.match(sNDC)):    
                sNDC_11 = sNDC[0:6] + '0' + sNDC[6:]
            elif (p_5_4_1.match(sNDC)):    
                sNDC_11 = sNDC[0:11] + '0' + sNDC[11:]
            elif (p_5_4_2.match(sNDC)):  
                print("This is a valid NDC") 
                sNDC_11 = sNDC
            elif (p_11.match(sNDC)):   
                sNDC_11 = sNDC[0:5]+ '-' + sNDC[5:9] + '-' + sNDC[9:]    
            else:
                print ("invalid NDC")
                sNDC_11 = ""

            # Remove dashes if not checked
            if intChkbxIncludeDashes.get() != 1:
                sNDC_11 = sNDC_11.replace("-","")

            # Write output file
            fo.write(sNDC_11 + "\n")    

    # Close output file
    fo.close()

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
    global intChkbxIncludeDashes 

    ####################################################
    # Build window
    ####################################################
    MDIWnd= tk.Tk()
    MDIWnd.title("Convert NDC codes")
    MDIWnd.geometry("1100x300")

    lblHdr = tk.Label(MDIWnd, text='Convert NDC codes from 10 digit to 11 digit')
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
    lblInFile1Label = tk.Label(MDIWnd, text='Input File of 10 digit NDC codes:')
    lblInFile1Label.config(font=('helvetica', 10))
    lblInFile1Label.grid(row=1, column=2, sticky='e', pady=1)

    # Selected InFile1
    lblInFile1Text = tk.Label(MDIWnd, text="")
    lblInFile1Text.config(font=('helvetica', 10))
    lblInFile1Text.grid(row=1, column=3, sticky='w')

    ###############################
    # Select Output File 
    ###############################
    btnOutFile = tk.Button(text='Select File', command=lambda:sel_txt_file(lblOutFileText), bg='blue', fg='white', font=('helvetica', 8, 'bold'))
    btnOutFile.grid(row=3, column=1, padx=2, pady=3)

    lblOutFileLabel = tk.Label(MDIWnd, text='Output File:')
    lblOutFileLabel.config(font=('helvetica', 10))
    lblOutFileLabel.grid(row=3, column=2, sticky='e')

    # Selected Output File
    lblOutFileText = tk.Label(MDIWnd, text='')
    lblOutFileText.config(font=('helvetica', 10))
    lblOutFileText.grid(row=3, column=3, sticky='w')

    ########################################
    # Checkbox to do "ignore case" compares 
    ########################################
    intChkbxIncludeDashes=tk.IntVar()
    ckboxIgnoreCase = tk.Checkbutton(MDIWnd, text = "Include Dashes in NDC Codes", variable=intChkbxIncludeDashes)
    ckboxIgnoreCase.grid(row=5, column=3, sticky='w')

    ###############################
    # Buttons
    ###############################
    btnCompare = tk.Button(text='Convert NDC Codes in Input File', command=initiateConvertNDCAction, bg='blue', fg='white', font=('helvetica',10, 'bold'))
    btnCompare.grid(row=6, column=3, sticky='w', pady=10)

    ####################################
    # Process Window messages
    ####################################
    MDIWnd.mainloop()


if __name__ == "__main__":
    
    main()




