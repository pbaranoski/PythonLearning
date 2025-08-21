# utilCCPCreateDocCSVFiles.py
# Paul Baranoski - 10/4/2021

import os
import sys
#from numpy import exp
import pandas
import re
import pathlib
import datetime


in_dir = r"C:\Users\PaulBaranoski\OneDrive - Index Analytics\Documents\PythonLearning\PythonLearning"
out_dir = r"C:\Users\PaulBaranoski\OneDrive - Index Analytics\Documents\PythonLearning\PythonLearning"

strSearch = "shutil"

##################
# Main
# 1) iterate over directory
# 2) identify file and lines where search string if found
##################

outFile = os.path.join(out_dir,"SearchResults.txt")
outResults = open(outFile,"w")

fileList = (dirItem for dirItem in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir,dirItem)) )

for searchFile in fileList:
    #print (searchFile)
    idx = searchFile.find(".")

    if (searchFile[idx:] == ".py" or searchFile[idx:] == ".txt"):
        #print(searchFile)
        pass
    else:
        # Skip file
        continue

    inFile = os.path.join(in_dir,searchFile)
    
    with open(inFile,"r", errors="ignore") as inPYFile:
        inFilename = os.path.basename(inFile)
        #print(inFilename)
        in_recs = inPYFile.readlines()
        for in_rec in in_recs:
            fndIdx = in_rec.find(strSearch)
            if fndIdx >= 0:
                print(inFilename)
                #print(os.path.getmtime(inFilename))
                dttm = pathlib.Path(inFilename).stat().st_mtime
                print(datetime.datetime.fromtimestamp(dttm).strftime("%Y-%m-%d-%H:%M:%S"))
                outResults.writelines(inFilename + "-->" + in_rec)
                #print(in_rec)

    # Close input file when done
    inPYFile.close()

outResults.close()

