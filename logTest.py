#!/usr/bin/env python
# python log learning

import sys
import os
import datetime
import re

log_dir = "/home/pbaranoski/Scripts/logs"

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

# Function for natural sorting of input file names so files are processed in numerical order
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

########################################
# test1
########################################
in_csvlist = "/home/pbaranoski/Scripts/csvlist.txt"

substr = in_csvlist[6:16]
print ("substr: "+substr)

with open(in_csvlist) as csvlist_obj:
    csvlist = csvlist_obj.readlines()
    csvlist = [i.strip("\n") for i in csvlist]
orig_files = [f for f in csvlist if os.path.exists(f)]
print ("orig_files: " + str(orig_files))

orig_files.sort(key=alphanum_key)
print ("len(orig_files):" + str(len(orig_files)))

if len(orig_files) == 0:
    print(". Quitting program.")
    exit(0)

########################################
# test2
########################################
print (sys.argv[0])
print (os.path.dirname(sys.argv[0]))
#os.mkdir(os.path.join(os.path.dirname(sys.argv[0]),"newLogs"))

csv_name = "/home/pbaranoski/Scripts/test.csv"
write_log("Error::Skipped[{}]".format(os.path.basename(csv_name)))
print ("Error::Skipped[{}]".format(os.path.basename(csv_name)))


########################################
# test3
########################################
with open(in_csvlist) as fobj:
    count = len(fobj.readlines())

print ("csvlist file count: "+str(count))




