# utilCCPConcatCSVs.py
# Paul Baranoski 10/4/2021

import os
import sys
import pandas

in_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCP documentation\OutFiles"
out_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCP documentation\FinalOutFiles"


##################
# Main
# 1) iterate over output directory's project sub-directories.
# 2) for each project sub-directory, process each .csv file, and combine into temp file in same directory.
# 3) Add project name as column, remove duplicate rows, and write new combined .csv file
##################
def main():

    # Get list of Project directories (i.e., BLUE_BUTTON, PECOS)
    projDirBaseList = (projDirBase for projDirBase in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir,projDirBase)) )

    # Iterate Project directories
    for projDirBase in projDirBaseList:

        # Create temp output filename in project directory to combine CSVs into    
        outTempFile = "temp_CombinedTemp.csv"
        out_file = os.path.join(out_dir, outTempFile)

        ofTempcsv = open(out_file,"w")
        # write header
        ofTempcsv.writelines("Schema,Table,ColName,Symbol\n")

        # Process input files in project directory
        projDirPath = os.path.join(in_dir,projDirBase)

        fileCSVList = (inCSVFile for inCSVFile in os.listdir(projDirPath) if os.path.isfile(os.path.join(projDirPath,inCSVFile)) )

        for inCSVFile in fileCSVList:
            #print(inCSVFile)
            in_file = os.path.join(projDirPath,inCSVFile)
    
            with open(in_file,"r") as ifcsv:
                inrecs = ifcsv.readlines()
                ofTempcsv.writelines(inrecs)
                ifcsv.close()  

        # Close temp output file when all input files have been concatenated into it
        ofTempcsv.close()

             
        tempDF = pandas.read_csv(out_file, sep=',', skip_blank_lines=True)
        print(tempDF)
        tempDF = tempDF.drop("Symbol",axis=1)
        # insert column as 1st column
        tempDF.insert(0,"PROJECT_NAME",value=projDirBase)
        # Assign column value in Data Frame
        tempDF["PROJECT_NAME"] = projDirBase

        #subset=["Schema","Table","ColName", "PROJECT_NAME"]
        tempDF = tempDF.drop_duplicates(subset=["PROJECT_NAME", "Schema","Table","ColName"])
        
        tempDF = tempDF.sort_values(by=['Schema', 'Table','ColName'], axis=0, ascending=True, kind='mergesort')

        print(tempDF)

        finalFilename = projDirBase + ".csv"
        final_out_file = os.path.join(out_dir, finalFilename)

        tempDF.to_csv(final_out_file, sep=',',index=False)


#####################
# execute program
#####################
if __name__ == "__main__":
    main()



      
