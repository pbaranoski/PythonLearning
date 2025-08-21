# utilCCPConcatCSVs.py
# Paul Baranoski 10/4/2021

import os

in_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCR documentation\FinalOutFiles"
out_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCR documentation\FinalDoc"

skip_header=True

##################
# Main
# 1) iterate over output directory's project sub-directories.
# 2) for each project sub-directory, process each .csv file, and combine into temp file in same directory.
# 3) Add project name as column, remove duplicate rows, and write new combined .csv file
##################
def main():

    # Create temp output filename in project directory to combine CSVs into    
    outTempFile = "ETL_CCP_Input_Temp.csv"
    out_file = os.path.join(out_dir, outTempFile)

    ofTempcsv = open(out_file,"w")

    # Process input files in project directory
    fileCSVList = (inCSVFile for inCSVFile in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir,inCSVFile)) )

    for inCSVFile in fileCSVList:
        #print(inCSVFile)
        in_file = os.path.join(in_dir,inCSVFile)

        with open(in_file,"r") as ifcsv:
            if skip_header:
                ifcsv.readline()

            inrecs = ifcsv.readlines()
            ofTempcsv.writelines(inrecs)
            ifcsv.close()  

    # Close temp output file when all input files have been concatenated into it
    ofTempcsv.close()


#####################
# execute program
#####################
if __name__ == "__main__":
    main()
    print("Program completed.")



      
