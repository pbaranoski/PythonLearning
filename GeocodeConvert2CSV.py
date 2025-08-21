import os
import sys
import traceback
import csv
import shutil
# Not found by pylance
# Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
# built on top of the Python programming language.
##import pandas

temp_input = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input"
out_dir = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\OutfolderPath"

in_indicator = 'IDRDGISD'# input file indicator
out_indicator ='GISDIDRD'# output file indicator
in_overwrite = True# True if output should be overwritten

#########################################################
# functions
#########################################################
def check_output(csv_name):
    result = True
    output_csv = os.path.join(out_dir,  os.path.basename(csv_name))
    # date1 = datetime.datetime.now()
    #output_csv = output_csv.replace(in_indicator,out_indicator)+ date1.strftime("%y%m%d")+ ".T" + date1.strftime("%H%M%S%f")[:-5] +".csv"
    output_csv = output_csv.replace(in_indicator,out_indicator)
    if os.path.exists(output_csv):
        if in_overwrite:
            result = True
        else:
            ##write_log("Error::Skipped[{}]".format(os.path.basename(csv_name)))
            print("Error::Skipped[{}]".format(os.path.basename(csv_name)))
            result = False

    return result

# Function to determins number of rows in input and output
def get_file_recordcount(in_file):
    with open(in_file,"r") as fobj:
        count = len(fobj.readlines())-1
    return count

# Pre-process function to add FID column to input csv for geocoding, output is comma-seperated
## Paul --> the output csv from the csv.writer appears to have an extra 'CR' 
## so each record ends in 'CR CR LF'
def convert_input_tocsv_fid(in_file):
    try:
        with open(in_file,"r") as fobj:
            with open(os.path.join(temp_input, "FID_"+os.path.basename(in_file)),"w") as outfobj:
                in_addresses = fobj.readlines()
                writer = csv.writer(outfobj, quoting = csv.QUOTE_ALL)
                all_rows = []
                for i in range(0, len(in_addresses)):
                    row = in_addresses[i].replace("\n","").strip().split("\t")
                    row = [item.strip('"') for item in row] #remove quotes from beg and end of each item

                    if i == 0:
                        row.append("FID") #inserts FID column
                        writer.writerow(row)
                        header_row = row
                    else:
                        row.append(i) #inserts FID
                        all_rows.append(row)
                writer.writerows(all_rows)
                outfobj.close()
        print ("filename: "+outfobj.name)
        return outfobj.name
    except:
        print (traceback.format_exc())

#########################################################
# Build in_files
#########################################################
in_csvlist = "C:/Users/user/Documents/PythonLearning/LandingDir/InfolderPath/csvlist.txt"

with open(in_csvlist) as csvlist_obj:
     # readlines gets all records at once
     # readline gets a record at a time
     # read gets the whole file or X # of bytes
    csvlist = csvlist_obj.readlines()
    csvlist = [i.strip("\n") for i in csvlist]

orig_files = [f for f in csvlist if os.path.exists(f)]

orig_files.sort()  
#print ("orig_files: "+str([f for f in orig_files]))  
print()

in_files = []
for f in orig_files:
    orginal_file = ""
    orginal_file = os.path.basename(f)
    # do not now what the real csv filenames are named
    # includes the extension as part of the filename "_ext" then adds .csv as the new extension
    dest = os.path.join(temp_input,os.path.basename(f).replace(".","_"))
    # Did the real filenames end in csv already?  I guess not. Maybe we can get some examples of what
    # the input files are named?
    dest = dest.replace("#","_") +".csv"

    if os.path.exists(f):
        # requires the import file "shutil"
        # this is shell utility.  Using the operating system functions.
        shutil.copy(f,dest)
        in_files.append(dest)
    else:
        write_log("Error::Input Missing[{}]".format(os.path.basename(f)))
        print("Error::Input Missing[{}]".format(os.path.basename(f)))

#########################################################
# create csv files.
#########################################################
for csvf in in_files:
        count_origin = get_file_recordcount(csvf) #debug for count
        ##print ("Original CSV Records {}".format(str(count_origin))) #debug for count

        # check if output does not exists, proceed if true
        if check_output(csvf):

            # convert tabbed csv to csv with FID
            in_csv = convert_input_tocsv_fid(csvf)

 