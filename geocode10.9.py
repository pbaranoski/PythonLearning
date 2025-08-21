#import required modules
import os
import io
#from contextlib import redirect_stderr
import sys
import datetime
import arcpy
from arcpy import management
from arcpy import geocoding
import traceback
import csv
import shutil
import re
import pandas

# Get parameters
in_csvlist = sys.argv[1]# input text file with list of csvs to process
addr_loc = sys.argv[2]# the address locator
input_dir = sys.argv[3]# input file location
out_dir = sys.argv[4]# location to create output
in_overwrite = True if sys.argv[5] == "True" else False# True if output should be overwritten
log_dir = sys.argv[6]# location for creating logs
in_indicator = sys.argv[7]# input file indicator
out_indicator = sys.argv[8]# output file indicator

# in_csvlist = r'C:/etl/work/geocodelist.lst'# input text file with list of csvs to process
# addr_loc = r'E:/USA/USA.loc'# the address locator
# input_dir = r'C:/etl/input' # input file location
# out_dir = r'C:/etl/output'# location to create output
# in_overwrite = False# True if output should be overwritten
# log_dir = r'C:/etl/work/logs'# location for creating logs
# in_indicator = 'IDRPGISP'# input file indicator
# out_indicator ='GISPIDRP'# output file indicator

# Build field mappings for locator
input_mappings = {"Address or Place": "ADDRESS",
				   "Address2":"<None>",
				   "Address3":"<None>",
                   "Neighborhood":"<None>",
                   "City":"CITY",
                   "State" : "REGION",
                   "ZIP" : "POSTAL",
                   "ZIP4": "POSTALEXT",
				   "Country":"<None>"
                  }
Preferred_Location_Type = 'ROUTING_LOCATION'
Output_Fields = 'ALL'

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
            #print(("Error::Skipped[{}]".format(os.path.basename(csv_name))))
            result = False

    return result

# Pre-process function to add FID column to input csv for geocoding, output is comma-seperated
def convert_input_tocsv_fid(in_file):
    try:
        with open(in_file,"r") as fobj:
            with open(os.path.join(temp_input, "FID_"+os.path.basename(in_file)),"w", newline="") as outfobj:
                in_addresses = fobj.readlines()
                writer = csv.writer(outfobj, quoting = csv.QUOTE_ALL)
                all_rows = []
                for i in range(0, len(in_addresses)):
                    row = in_addresses[i].strip().split("\t")
                    row = [item.strip('"') for item in row] #removing extra quotes
                    if i == 0:
                        row.append("FID") #inserts FID column
                        writer.writerow(row)
                        header_row = row
                    else:
                        row.append(i) #inserts FID
                        all_rows.append(row)
                writer.writerows(all_rows)
                outfobj.close()
        return outfobj.name
    except:
        print((traceback.format_exc()))

# Function to convert the geocoded GDB output table to tab delimited csv with geocoded fields and FID
# updated create_output_csv fuction to work for ArcGIS 10.8

def create_output_csv(input_table):
    try:

        if not arcpy.Exists(input_table):
            return None
        # writes out only geocode fields
        fields = ["USER_FID", "SCORE", "MATCH_ADDR", "ADDR_TYPE", "DISPLAYX", "DISPLAYY"]
        fields1 = ["FID", "SCORE", "MATCH_ADDR", "ADDR_TYPE", "DISPLAYX", "DISPLAYY"]
        rows = arcpy.SearchCursor(input_table, fields, sort_fields="USER_FID A")
        out_file = os.path.join(temp_output,"FID"+os.path.basename(input_table)+ ".csv")
        with open(out_file,"w") as outfobj:
            outfobj.write('"'+'","'.join(fields1)+'"\n') #writes the column names
            for row in rows:
                line = []
                tab_out_addr = []
                line.append( '"'+ str(row.getValue("USER_FID"))
                              +'"'+ ',' +'"'+ str(row.getValue("SCORE"))
                              +'"'+ ',' +'"'+ str(row.getValue("MATCH_ADDR"))
                              +'"'+ ',' +'"'+ str(row.getValue("ADDR_TYPE"))
                              +'"'+ ',' +'"'+ str(row.getValue("DISPLAYX"))
                              +'"'+ ',' +'"'+ str(row.getValue("DISPLAYY"))
                             +'"\n')

            #     #convert to tabbed
                tab_out_addr.append('"\t"'.join(line))
                outfobj.writelines(list(map(str, tab_out_addr)))
            outfobj.close()
        return out_file
    except:
        print((traceback.format_exc()))

# Function to merge the output geocoded fields with input csv and drop FID column
def merge_csvs(out_csv, in_csv):
    try:
        dtype_dict = {"POSTAL": str, "POSTALEXT": str}
        out_df = pandas.read_csv(out_csv,na_filter=False, warn_bad_lines=True, error_bad_lines=False)
        in_df = pandas.read_csv(in_csv, dtype = dtype_dict, na_filter=False, warn_bad_lines=True, error_bad_lines=False)
        merged_csv = out_csv.replace("FID","")
        out_df = out_df.merge(in_df)
        out_df = out_df.drop("FID",axis=1)
        #workaround for quoting issue, pandas df treats POSTALEXT as numeric so expllicity converting to string
        fields = ["SCORE", "DISPLAYX", "DISPLAYY", "POSTALEXT"]
        for cols in out_df:
            if cols in fields:
                out_df[cols] = out_df[cols].astype(str)

        out_df.to_csv(merged_csv,sep = "\t", index=False, line_terminator = "\n", quoting=csv.QUOTE_NONNUMERIC)

        return merged_csv
    except:
        print((traceback.format_exc()))

# Function to determins number of rows in input and output
def get_file_recordcount(in_file):
    with open(in_file,"r") as fobj:
        count = len(fobj.readlines())-1
    return count


# Function to clean up temp files after each input file is processed
def clean_up(csv_name):
    try:
        temp_fc = os.path.join(temp_gdb,os.path.basename(csv_name)[:-4])
        if arcpy.Exists(temp_fc): arcpy.management.Delete(temp_fc)
        if os.path.basename(csv_name).lower().find(in_indicator) >= 0:

            csv_name = os.path.basename(csv_name).lower().split(in_indicator)[1]

        temp_infiles = get_tempfile(csv_name, temp_input)
        temp_outfiles = get_tempfile(csv_name, temp_output)
        for f in temp_infiles+temp_outfiles: os.remove(f)
    except Exception as ex:
        print((traceback.format_exc()))


# Function to return list of temp files created during the process for clean-up
def get_tempfile(file_name, temp_dir):
    file_list = []
    for f in os.listdir(temp_dir):
        if f.find(os.path.basename(file_name)) >= 0:
            file_list.append(os.path.join(temp_dir,f))
    return file_list


# Function to write logs. Depending on the status log messages will be written to Errors.txt or Messages.txt
def write_log(msg):
    error_file = os.path.join(log_dir,"Errors.txt")
    message_file = os.path.join(log_dir,"Messages.txt")
    log_fields = ["TimeStamp", "Status", "File", "Message"]
    # status of the process
    status_details = {"Started": "Geocoding started.",
              "Skipped": "Input file row was skipped",
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
    ocsv2 = ocsv2 = ocsv2[:22]+ "F" + ocsv2[23: -4] # newly added code on 05/07/2020
    ocsv2 = ocsv2
    shutil.copy(in_csv, os.path.join(out_dir, os.path.basename(ocsv2)))
    write_log("Error::Failed[{}]".format(os.path.basename(ocsv2)))
    #print(("Error::Failed[{}]".format(os.path.basename(ocsv2))))

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
    print("Started at [{}]".format(datetime.datetime.now()))
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
    temp_wksp = temp_wksp.replace("\\","/")
    temp_input = os.path.join(temp_wksp,"temp_input")
    temp_input = temp_input.replace("\\", "/")
    temp_output = os.path.join(temp_wksp, "temp_output")
    temp_output = temp_output.replace("\\", "/")
    temp_gdb = os.path.join(temp_wksp,"geocode_out.gdb")
    temp_gdb = temp_gdb.replace("\\", "/")

    if not os.path.exists(temp_wksp):
        os.mkdir(temp_wksp)

    if not os.path.exists(temp_input):
        os.mkdir(temp_input)

    if arcpy.Exists(temp_gdb):
        arcpy.management.Delete(temp_gdb)

    if not os.path.exists(temp_output):
        os.mkdir(temp_output)

    arcpy.management.CreateFileGDB(os.path.dirname(temp_gdb), os.path.basename(temp_gdb))

    # make log folder
    logdate = datetime.datetime.now()

    log_dir = arcpy.CreateUniqueName("geocode"+logdate.strftime("%y%m%d")+"logs" ,log_dir)
    log_dir =log_dir.replace("\\","/")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # copy input files to temp location
    in_files = []
    for f in orig_files:
        #orginal_file = ""
        orginal_file = os.path.basename(f)
        dest = os.path.join(temp_input,os.path.basename(f).replace(".","_"))
        dest = dest.replace("\\","/")
        dest = dest.replace("#","_") +".csv"
        if os.path.exists(f):
            shutil.copy(f,dest)
            in_files.append(dest)
        else:
            write_log("Error::Input Missing[{}]".format(os.path.basename(f)))
            #print(("Error::Input Missing[{}]".format(os.path.basename(f))))

    # proceed to geocode
    for csvf in in_files:
        count_origin = get_file_recordcount(csvf) #debug for count
        #print(("Original CSV Records {}".format(str(count_origin)))) #debug for count

        # check if output does not exists, proceed if true
        if check_output(csvf):
            csvf = csvf.replace("\\","/")
            # convert tabbed csv to csv with FID
            in_csv = convert_input_tocsv_fid(csvf)
            in_csv = in_csv.replace("\\", "/")
            tempin_count = get_file_recordcount(in_csv) #debug for count
            #print(("Temp Input CSV Records {}".format(str(tempin_count)))) #debug for count
            feature_class_name = os.path.basename(in_csv)[4:-4]
            out_feature_class = os.path.join(temp_gdb, feature_class_name)
            out_feature_class = out_feature_class.replace("\\","/")
            input_csv = os.path.join(temp_input, 'input_csv.csv')
            input_csv = input_csv.replace("\\","/")
            #print(input_csv)
            f = io.StringIO()
            with redirect_stderr(f):
                in_df = pandas.read_csv(in_csv, na_filter=False, warn_bad_lines=True, error_bad_lines=False, low_memory=False)
            if f.getvalue():
                #print("Parsing Error: {}".format(f.getvalue()))
                write_log("Error::Skipped[{}]".format(f.getvalue()))

            in_df.to_csv(input_csv, sep="\t", index=False, line_terminator="\n", quoting=csv.QUOTE_NONNUMERIC)
            csvf1 = replace_str_index(os.path.basename(csvf), 1, '#')
            csvf1 = csvf1.replace("_", ".")
            csvf1 = csvf1[:-4]
            write_log("Message::Started[{}]".format(csvf1))
            #print(("Message::Started[{}]".format(csvf1)))

            try:
                result = arcpy.geocoding.GeocodeAddresses(input_csv, addr_loc, addr_fields, out_feature_class, 'STATIC', None, Preferred_Location_Type, None, Output_Fields)
                #print("Geocoded")
                geocoded_tablecount = arcpy.management.GetCount(out_feature_class)[0] #debug for count
                #print(("Geocoded Table Records {}".format(str(geocoded_tablecount)))) #debug for count
            # if geocoding fails copy input and write error to log
            except arcpy.ExecuteError:
                #print(arcpy.GetMessages())
                csvf1 = csvf.replace('P.','F.')
                #cf = os.rename(csvf,csvf1)
                write_log("Message::Failed[{}]".format(0))
                copy_failedcsv(csvf1)
                clean_up(csvf1)
                continue

            # if success, convert feature class to tab delimited csv sorted by FID
            out_csv = create_output_csv(out_feature_class)
            out_csv = out_csv.replace("\\","/")
            if out_csv is not None:

                # out csv is merged with input, FID removed
                out_csv= merge_csvs(out_csv, in_csv)

                # check output count matches input, if true make signal and copy output
                out_csv_count = get_file_recordcount(out_csv)
                ocsv = replace_str_index(os.path.basename(out_csv), 1, '#')
                ocsv = ocsv.replace("_", ".")
                ocsv = ocsv.replace(in_indicator, out_indicator)
                ocsv = ocsv[:-4]
                # print ocsv
                #print(("Output CSV Records {}".format(str(out_csv_count)))) #debug for count
                write_log("Message::Completed[{}]::{}".format(ocsv, out_csv_count))
                #print(("Message::Completed[{}]::{}".format(ocsv, out_csv_count)))
                shutil.copy(out_csv, os.path.join(out_dir,ocsv))
                clean_up(out_csv)
            else:
                copy_failedcsv(csvf)
                continue
    print(("logs avaialable at: {}".format(log_dir)))

except Exception:
    print((traceback.format_exc()))

finally:
   try:
       if os.path.exists(temp_wksp): shutil.rmtree(temp_wksp)
   except:
       pass
print("Ended at [{}]".format(datetime.datetime.now()))
#print("done")
