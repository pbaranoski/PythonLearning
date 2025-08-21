# ------------------------------------------------------------------------------
# name: geocode.py
#
# Description: Script to geocode in batch tab delimitted csv files
# - This script works with 64 bit python and
#   64 bit geocode_addresses tool accessible either with
#   ArcGIS Server or 64 bit Background geprocessing
# - It parses the input file list, copies input csv files
#   ready to be geocded to a temprary location in the location of the script.
# - After processing is complete output is copied to the output location
#
#
# Usage: To run this script you will need to pass 7 parameters
# 1. Input csv list: (string) a text file with a list of csv file names
#    that are ready to be processed
# 2. Input address locator: (string) the path to the address locator
# 3. Output directory: (string) a folder path where output *output file indicator*.csv
# 4. Overwrite output: (string) "True" or "False" to indicate
#    whether existing output can be overwritten
# 5. Log directory: (string) a folder path where logs can be generated.
# 6. input file indicator: (string) indicates an input file
# 7. output file indicator: (string) indicates an output file.

# Process:
# - Input csv list file is scanned, for each csv name in this file, we check if
#   the input csv list file. If yes we make a copy of the csv to temp input workspace
#   and use this copy for geocoding.
# - For each item in temp input we first ensure no output is already created.
#   If no output then we pre-process the file for geocoding.
# - Pre-processing includes adding an "FID" value to the records in the CSV. This
#   is temporary process and is removed before final output.
# - Geocoding results are stored in a temp geodatabase and are converted to
#   csv in a temp output location for post processing
# - Post process includes sorting by temp FID values added so the records line up
#   to be same as input. Geocoded values from the output are merged with
#   the input attributes.
# - If the number of geocoded records match the orignal input then the output is
#   copied to the user defined output location with the output file indicator in csv filename indicating
#   completion of process.
# - All the temp locations and files are stored at the location of this script.
#   Note: Since tempoorary files are created in the location of this script file
#   python must have write permission to the directory where this script is saved.
#
# ----------------------------------------------------------"--------------------


#import required modules
import os
import sys
import datetime
import arcpy
import traceback
import csv
import shutil
import re
import pandas
import difflib

# Get parameters
# in_csvlist = sys.argv[1]# input text file with list of csvs to process
# addr_loc = sys.argv[2]# the address locator
# input_dir = sys.argv[3]# input file location
# out_dir = sys.argv[4]# location to create output
# in_overwrite = True if sys.argv[5] == "True" else False# True if output should be overwritten
# log_dir = sys.argv[6]# location for creating logs
# in_indicator = sys.argv[7]# input file indicator
# out_indicator = sys.argv[8]# output file indicator

in_csvlist = 'C:\etl\work\geocodelist.lst'# input text file with list of csvs to process
addr_loc = 'E:\locator\CMS_Locator.loc'# the address locator
input_dir = 'C:\etl\input' # input file location
out_dir = 'C:\etl\output'# location to create output
in_overwrite = False# True if output should be overwritten
log_dir = 'C:\etl\work\logs'# location for creating logs
in_indicator = 'IDRDGISD'# input file indicator
out_indicator ='GISDIDRD'# output file indicator

# Build field mappings for locator
input_mappings = {"Address": "ADDRESS",
                   "Neighborhood":"<None>",
                   "City":"CITY",
                   "Region" : "REGION",
                   "Postal" : "POSTAL",
                   "PostalExt": "POSTALEXT"
                  }

addr_fields = arcpy.FieldInfo()


for field in input_mappings:
    addr_fields.addField(field, input_mappings[field], "VISIBLE", "NONE")


# Function to check if output exist and if overwrite is true
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
            write_log("Error::Skipped[{}]".format(os.path.basename(csv_name)))
            print("Error::Skipped[{}]".format(os.path.basename(csv_name)))
            result = False

    return result


# Pre-process function to add FID column to input csv for geocoding, output is comma-seperated
## Paul --> DO input files have a HEADER record?
def convert_input_tocsv_fid(in_file):
    try:
        with open(in_file,"r") as fobj:
            with open(os.path.join(temp_input, "FID_"+os.path.basename(in_file)),"w") as outfobj:
                in_addresses = fobj.readlines()
                writer = csv.writer(outfobj, quoting = csv.QUOTE_ALL)
                all_rows = []
                # Paul --> for each address record
                for i in range(0, len(in_addresses)):
                    ## Paul --> Row is an array of fields
                    ## Paul --> these two lines can be combined. May increase performance
                    row = in_addresses[i].strip().split("\t")
                    row = [item.strip('"') for item in row] #removing extra quotes
                    # Paul --> write header; FID column would be last column
                    if i == 0:
                        row.append("FID") #inserts FID column
                        writer.writerow(row)
                        header_row = row
                    else:
                        # Paul --> i is a sequence #; added to the end of row
                        row.append(i) #inserts FID
                        all_rows.append(row)
                # Paul write all records for csv file at once        
                writer.writerows(all_rows)
                outfobj.close()
        return outfobj.name
    except:
        print traceback.format_exc()


# Function to convert the geocoded GDB output table to tab delimited csv with geocoded fields and FID
# updated create_output_csv fuction to work for ArcGIS 10.8

def create_output_csv(input_table):
    try:
        
        if not arcpy.Exists(input_table):
            return None
        # writes out only geocode fields
        dataList = arcpy.ListFields(input_table) # updated code for ArcGIS 10.8

        fields = ["FID", "SCORE", "MATCH_ADDR","ADDR_TYPE","DISPLAYX", "DISPLAYY"]
        #fields = [dataList[60].name.upper(),dataList[4].name.upper(),dataList[6].name.upper(),dataList[8].name.upper(),dataList[24].name.upper(),dataList[25].name.upper()] # updated code for ArcGIS 10.8 
		# print fields
        rows = arcpy.da.SearchCursor(input_table, field_names=fields)
        out_file = os.path.join(temp_output,"FID"+os.path.basename(input_table)+ ".csv")
        with open(out_file,"w") as outfobj:
            #fields = [dataList[60].name.upper()[:3],dataList[4].name.upper(),dataList[6].name.upper(),dataList[8].name.upper(),dataList[24].name.upper(),dataList[25].name.upper()] #updated code for ArcGIS 10.8
            ## Paul --> write header record
            outfobj.write('"'+'"\t"'.join(fields)+'"\n') #writes the column names
            ## Paul --> \/\/\/
            ##outfobj.write('"'.join('"\t"').join(fields).join('"\n')) #writes the column names

            ## Paul out_addr is an array            
            out_addr = [row for row in rows]

            # all the rows sorted by FID to match up with input csv
            sorted_out_addr = sorted(out_addr, key=lambda tup: int(tup[0]))# updated code for ArcGIS 10.8

            #sort by FID
            tab_out_addr = []

            # encode address parts if needed
            for addr in sorted_out_addr:
                line = []
                for v in addr:
                    if isinstance(v, unicode):
                        line.append(v.encode('utf-8'))
                    else:
                        line.append(str(v))

                #convert to tabbed
                tab_out_addr.append('"'+'"\t"'.join(line)+'"\n')
                ## Paul -->
                tab_out_addr.append('"'.join('"\t"').join(line).join('"\n'))

            outfobj.writelines(map(str, tab_out_addr))
            outfobj.close()
        return out_file
    except:
        print traceback.format_exc()

# Function to merge the output geocoded fields with input csv and drop FID column
def merge_csvs(out_csv, in_csv):
    # processed_lines_log = os.path.join(log_dir, "processed_lines.csv")
    # in_file = os.path.join(log_dir, "infile.csv")
    # out_file = os.path.join(log_dir, "outfile.csv")
    # skipped_lines_log = os.path.join(log_dir, "skipped_lines.csv")

    # with open(processed_lines_log, 'w') as fp:
    try:
        dtype_dict = {"POSTAL": str, "POSTALEXT": str}
        out_df = pandas.read_csv(out_csv,sep = "\t", na_filter=False, warn_bad_lines=True, error_bad_lines=False)
        in_df = pandas.read_csv(in_csv, dtype = dtype_dict, na_filter=False, warn_bad_lines=True, error_bad_lines=False)
        # result = in_df.apply(pandas.to_numeric, errors='ignore', axis=1)
        # # print result
        # df = pandas.DataFrame
        # df = result
        # df.to_csv(fp, quoting=csv.QUOTE_ALL, sep='\t', lineterminator='\r', index=False)
        # fp.close()
        merged_csv = out_csv.replace("FID","")
        out_df = out_df.merge(in_df)     # Getting Error Message Here before fixing after ArcGIS 10.8 upgrade
        out_df = out_df.drop("FID",1)
        #workaround for quoting issue, pandas df treats POSTALEXT as numeric so expllicity converting to string
        fields = ["SCORE", "DISPLAYX", "DISPLAYY", "POSTALEXT"]
        for cols in out_df:
            if cols in fields:
                out_df[cols] = out_df[cols].astype(str)

        out_df.to_csv(merged_csv,sep = "\t", index=False, line_terminator = "\n", quoting=csv.QUOTE_NONNUMERIC)

        return merged_csv
    except:
        print traceback.format_exc()

# Function to determins number of rows in input and output
def get_file_recordcount(in_file):
    ## Paul do not count header record
    with open(in_file,"r") as fobj:
        count = len(fobj.readlines())-1
    return count


# Function to clean up temp files after each input file is processed
def clean_up(csv_name):
    try:
        # Remove extention ".csv" ?
        temp_fc = os.path.join(temp_gdb,os.path.basename(csv_name)[:-4])
        if arcpy.Exists(temp_fc): arcpy.Delete_management(temp_fc)

        ## Paul --> what is the purpose of this IF?  in_indicator is upper-cased.  
        ## Paul --> How can it find the string?
        if os.path.basename(csv_name).lower().find(in_indicator) >= 0:

            csv_name = os.path.basename(csv_name).lower().split(in_indicator)[1]

#        elif os.path.basename(csv_name).lower().find("idr") >= 0:
#            csv_name = os.path.basename(csv_name).lower().split("idr")[1]

        temp_infiles = get_tempfile(csv_name, temp_input)
        temp_outfiles = get_tempfile(csv_name, temp_output)
        for f in temp_infiles+temp_outfiles: os.remove(f)

    except Exception as ex:
        print traceback.format_exc()


# Function to return list of temp files created during the process for clean-up
def get_tempfile(file_name, temp_dir):
    file_list = []
    for f in os.listdir(temp_dir):
        if f.find(os.path.basename(file_name)) >= 0:
            file_list.append(os.path.join(temp_dir,f))
##    print "Files getting cleaned up" #debug
##    print file_list #debug
    return file_list


# Function to write logs. Depending on the status log messages will be written to Errors.txt or Messages.txt
def write_log(msg):
    error_file = os.path.join(log_dir,"Errors.txt")
    message_file = os.path.join(log_dir,"Messages.txt")
    log_fields = ["TimeStamp", "Status", "File", "Message"]
    # status of the process
    status_details = {"In Progress": "Geocoding started.",
              "Skipped": "Input was skipped. Ouput already exists.",
              "Failed": "Geocoding failed.",
              "Mismatch": "Counts between input and output dont match.",
              "Completed": "Geocoding completed ({} records processed).",
              "Input Missing" : "No corresponding csv file for signal file"
        }
    log_details = []
    date = datetime.datetime.now()
    time_stamp = date.strftime("%m/%d/%Y %H:%M:%S")
    log_details.append(time_stamp)
    msgarr = msg.split("::")
    status= msgarr[1][:msgarr[1].find("[")]
    log_details.append(status)
    file_name = msgarr[1][msgarr[1].find("[")+1:msgarr[1].find("]")]
    log_details.append(file_name)
    status_msg = status_details.get(status)
    if len(msgarr) > 2:
        status_msg = status_msg.format(str(msgarr[2]))
    log_details.append(status_msg)
    if msgarr[0]=="Error":
        if not os.path.exists(error_file):
            fobj = open(error_file,"w")
            fobj.write(",".join(log_fields)+"\n")
            fobj.close()
        fobj = open(error_file,"a")
    elif msgarr[0] == "Message":
        if not os.path.exists(message_file):
            fobj = open(message_file,"w")
            fobj.write(",".join(log_fields)+"\n")
            fobj.close()
        fobj = open(message_file,"a")
    fobj.write(",".join(log_details)+"\n")
    fobj.close()


# Function to copy input file to error folder in log directory if geogoding status is Failed
def copy_failedcsv(in_csv):
    ocsv2 = replace_str_index(os.path.basename(in_csv), 1, '#')
    ocsv2 = ocsv2.replace("_", ".")
    ocsv2 = ocsv2.replace(in_indicator, out_indicator)
    #ocsv2 = ocsv2.replace("P.","F.")
    #date2 = datetime.datetime.now()
    #ocsv2 = ocsv2[:25] + date2.strftime("%y%m%d") + ".T" + date2.strftime("%H%M%S%f")[:-5] + ".csv" 
    ocsv2 = ocsv2 = ocsv2[:22]+ "F" + ocsv2[23: -4] # newly added code on 05/07/2020
    #print ocsv2
    ocsv2 = ocsv2
    shutil.copy(in_csv, os.path.join(out_dir, os.path.basename(ocsv2)))
    write_log("Error::Failed[{}]".format(os.path.basename(ocsv2)))
    print("Error::Failed[{}]".format(os.path.basename(ocsv2)))

# Function to replace character at perticular string index
def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

# Function for natural sorting of input file names so files are processed in numerical order
def tryint(s):
    try:
        return int(s)
    except:
        return s

# Function for natural sorting of input file names so files are processed in numerical order
def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


# ------------------------------------------------------------------------------------------
# Main workflow
try:
    orginal_file = ""
    #sanity checks for existance of paths
    if not os.path.exists(out_dir):
        print("Incorrect output path. Quitting program.")
        exit(0)

    with open(in_csvlist) as csvlist_obj:
        csvlist = csvlist_obj.readlines()
        csvlist = [i.strip("\n") for i in csvlist]
    orig_files = [f for f in csvlist if os.path.exists(f)]
    orig_files.sort(key=alphanum_key)
    if len(orig_files) == 0:
        print(". Quitting program.")
        exit(0)

    # make temp folders in the script directory
    temp_wksp = arcpy.CreateUniqueName("temp_wksp",os.path.dirname(sys.argv[0]))

    temp_input = os.path.join(temp_wksp,"temp_input")
    temp_output = os.path.join(temp_wksp, "temp_output")
    temp_gdb = os.path.join(temp_wksp,"geocode_out.gdb")

    if not os.path.exists(temp_wksp):
        os.mkdir(temp_wksp)

    if not os.path.exists(temp_input):
        os.mkdir(temp_input)

    if arcpy.Exists(temp_gdb):
        arcpy.Delete_management(temp_gdb)

    if not os.path.exists(temp_output):
        os.mkdir(temp_output)

    arcpy.CreateFileGDB_management(os.path.dirname(temp_gdb), os.path.basename(temp_gdb))

    # make log folder
    logdate = datetime.datetime.now()

    log_dir = arcpy.CreateUniqueName("geocode"+logdate.strftime("%y%m%d")+"logs" ,log_dir)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # copy input files to temp location
    in_files = []
    for f in orig_files:
        orginal_file = ""
        orginal_file = os.path.basename(f)
        dest = os.path.join(temp_input,os.path.basename(f).replace(".","_"))
        dest = dest.replace("#","_") +".csv"
        if os.path.exists(f):
            shutil.copy(f,dest)
            in_files.append(dest)
        else:
            write_log("Error::Input Missing[{}]".format(os.path.basename(f)))
            print("Error::Input Missing[{}]".format(os.path.basename(f)))
##    print "{} files in temp input".format(str(len(in_files))) #debug for filecount

    # proceed to geocode
    for csvf in in_files:
        count_origin = get_file_recordcount(csvf) #debug for count
        print "Original CSV Records {}".format(str(count_origin)) #debug for count

        # check if output does not exists, proceed if true
        if check_output(csvf):

            # convert tabbed csv to csv with FID
            in_csv = convert_input_tocsv_fid(csvf)
            tempin_count = get_file_recordcount(in_csv) #debug for count
            print "Temp Input CSV Records {}".format(str(tempin_count)) #debug for count

            ## Paul --> (-4) removes '.csv'; what 4 bytes are we skipping in front?
            feature_class_name = os.path.basename(in_csv)[4:-4]
            out_feature_class = os.path.join(temp_gdb, feature_class_name)
            input_csv = os.path.join(temp_input, 'input_csv.csv')
            in_df = pandas.read_csv(in_csv, na_filter=False, warn_bad_lines=True, error_bad_lines=False, low_memory=False)
            in_df.to_csv(input_csv, sep="\t", index=False, line_terminator="\n", quoting=csv.QUOTE_NONNUMERIC)
            # geocoding with locators creates a unique output table in fgdb for each file
            #write_log("Message::In Progress[{}]".format(orginal_file))
            #print("Message::In Progress[{}]".format(orginal_file))
            csvf1 = replace_str_index(os.path.basename(csvf), 1, '#')
            csvf1 = csvf1.replace("_", ".")
            csvf1 = csvf1[:-4]
            write_log("Message::In Progress[{}]".format(csvf1))
            print("Message::In Progress[{}]".format(csvf1))
            try:
                result = arcpy.GeocodeAddresses_geocoding(input_csv, addr_loc,
                                                          addr_fields,
                                                          out_feature_class,
                                                          "STATIC")
                print ("Geocoded")
                geocoded_tablecount = arcpy.GetCount_management(out_feature_class)[0] #debug for count
                print "Geocoded Table Records {}".format(str(geocoded_tablecount)) #debug for count
            # if geocoding fails copy input and write error to log
            except arcpy.ExecuteError:
                #print(arcpy.GetMessages(2))
                csvf1 = csvf.replace('P.','F.')
                #cf = os.rename(csvf,csvf1)
                write_log("Message::Failed[{}]".format(0))
                copy_failedcsv(csvf1)
                clean_up(csvf1)
                continue


            # if success, convert feature class to tab delimited csv sorted by FID
            out_csv = create_output_csv(out_feature_class)
            if out_csv is not None:

                # out csv is merged with input, FID removed
                out_csv= merge_csvs(out_csv, in_csv)

                # check output count matches input, if true make signal and copy output
                out_csv_count = get_file_recordcount(out_csv)
                #if count_origin == out_csv_count:
                ocsv = replace_str_index(os.path.basename(out_csv), 1, '#')
                ocsv = ocsv.replace("_", ".")
                ocsv = ocsv.replace(in_indicator, out_indicator)
                #date3 = datetime.datetime.now()
                #ocsv = ocsv[:25] + date3.strftime("%y%m%d") + ".T" + date3.strftime("%H%M%S%f")[:-5] + ".csv"
                ocsv = ocsv[:-4]
                # print ocsv
                print "Output CSV Records {}".format(str(out_csv_count)) #debug for count
                write_log("Message::Completed[{}]::{}".format(ocsv, out_csv_count))
                print ("Message::Completed[{}]::{}".format(ocsv, out_csv_count))
                shutil.copy(out_csv, os.path.join(out_dir,ocsv))
                clean_up(out_csv)
                #else:
                    #write_log("Error::Mismatch[{}]".format(os.path.basename(out_csv)))
                    #print ("Error::Mismatch[{}]".format(os.path.basename(out_csv)))
                    #shutil.copy(out_csv, os.path.join(out_dir,os.path.basename(out_csv)))
                    #clean_up(out_csv)

                infile = os.path.join(input_dir,orginal_file)
                outfile = os.path.join(out_dir,ocsv)
                in_file = os.path.join(log_dir, "infile.csv")
                out_file = os.path.join(log_dir, "outfile.csv")
                skipped_lines_log = os.path.join(log_dir, orginal_file + "_Warnings.txt")
                with open(in_file, 'w') as fp1, open(out_file, 'w') as fp2:
                    try:
                        df1 = pandas.read_csv(infile, sep='\t', header=0, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], low_memory=False)
                        df1.to_csv(fp1, sep='\t', lineterminator='\r', index=False,quoting=csv.QUOTE_ALL)

                        df2 = pandas.read_csv(outfile, sep='\t', header=0, usecols=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], low_memory=False)
                        df2.to_csv(fp2, sep='\t', lineterminator='\r', index=False, quoting=csv.QUOTE_ALL)
                        fp1.close()
                        fp2.close()
                    except:
                        print traceback.format_exc()
                with open(in_file, 'r') as t1, open(out_file,'r') as t2:
                    fileone = t1.readlines()
                    filetwo = t2.readlines()
                with open(skipped_lines_log,'w') as fp1:
                    count = 0
                    for line in fileone:
                        count = count + 1
                        if line not in filetwo:
                            fp1.write("Row {}: {}".format(count, line))
                        else:
                            pass
                    fp1.close()
                    t1.close()
                    t2.close()
                    os.remove(in_file)
                    os.remove(out_file)

            else:
                copy_failedcsv(csvf)
                continue
    print("logs avaialable at: {}".format(log_dir))

except Exception:
    print traceback.format_exc()

finally:
    try:
        if os.path.exists(temp_wksp): shutil.rmtree(temp_wksp)
    except:
        pass

print("done")
