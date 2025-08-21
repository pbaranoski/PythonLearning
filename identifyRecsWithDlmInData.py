# Test stderr

import os
import io
import datetime
from contextlib import redirect_stderr
import pandas

in_dir = r"C:\Users\user\Documents\PythonLearning\LandingDir\temp_input"
log_dir = r"C:\Users\user\Documents\PythonLearning\LandingDir\logs"

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

##########################################
#  MAIN
##########################################    
#Additionally, for the Windows operating system, you can append ‘b’ 
# for accessing the file in binary. 
# This is is because Windows differentiates between a binary text file 
# and a regular text file.

in_csv = os.path.join(in_dir,"BadDlmFile3.csv")

# Define a file using StringIO
f = io.StringIO()
# redirect stderr to file (f) from io.StringIO() function
with redirect_stderr(f):
    in_df = pandas.read_csv(in_csv, na_filter=False, warn_bad_lines=True, error_bad_lines=False, low_memory=False)
if f.getvalue():
    print("f.getValue: "+f.getvalue())
    #print("Parsing Error: {}".format(f.getvalue()))
    write_log("Error::Skipped[{}]".format(f.getvalue()))

print(in_df)    