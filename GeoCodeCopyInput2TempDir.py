import os
import shutil
import datetime

in_csvlist = "C:/Users/user/Documents/PythonLearning/LandingDir/InfolderPath/csvlist.txt"

############################################
# function
############################################
def write_log(msg):
    error_file = os.path.join(log_dir,"Errors.txt")
    message_file = os.path.join(log_dir,"Messages.txt")
    log_fields = ["TimeStamp", "Status", "File", "Message"]
    # status of the process
    status_details = {"In Progress": "Geocoding started.",
              "Skipped": "Input was skipped. Output already exists.",
              "Failed": "Geocoding failed.",
              "Mismatch": "Counts between input and output dont match.",
              "Completed": "Geocoding completed ({} records processed).",
              "Input Missing" : "No corresponding csv file for signal file"
        }
    msgarr = msg.split("::")
    status= msgarr[1][:msgarr[1].find("[")]
    file_name = msgarr[1][msgarr[1].find("[")+1 : msgarr[1].find("]")]

    log_details = []
    date = datetime.datetime.now()
    time_stamp = date.strftime("%m/%d/%Y %H:%M:%S")
    log_details.append(time_stamp)
    log_details.append(status)
    log_details.append(file_name)

    if len(msgarr) > 2:
        status_msg = status_msg.format(str(msgarr[2]))
    else:
        status_msg = status_details.get(status)

    log_details.append(status_msg)

    # Open; write; close file; 
    if msgarr[0]=="Error":
        # Write out header - trigger --> file doesn't exist
        if not os.path.exists(error_file):
            fobj = open(error_file,"w")
            fobj.write(",".join(log_fields)+"\n")
            fobj.close()
        fobj = open(error_file,"a")
    # Write out header - trigger --> file doesn't exist
    elif msgarr[0] == "Message":
        if not os.path.exists(message_file):
            fobj = open(message_file,"w")
            fobj.write(",".join(log_fields)+"\n")
            fobj.close()
        fobj = open(message_file,"a")
    # write actual message    
    fobj.write(",".join(log_details)+"\n")
    fobj.close()

    return        


###########################################
# get list of input files
########################################### 
with open(in_csvlist) as csvlist_obj:
     # readlines gets all records at once
     # readline gets a record at a time
     # read gets the whole file or X # of bytes
    csvlist = csvlist_obj.readlines()
    csvlist = [i.strip("\n") for i in csvlist]

# orig_files only contains files that exist
orig_files = [f for f in csvlist if os.path.exists(f)]

if len(orig_files) == 0:
    print(". Quitting program.")
    exit(0)

orig_files.sort()  
print ("orig_files: "+str([f for f in orig_files]))  
print()

####################################
# copy input files to temp location
#####################################
input_dir = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir"
temp_input = os.path.join(input_dir,"temp_input")

if not os.path.exists(temp_input):
    os.mkdir(temp_input) 

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
        shutil.copy(f,dest)
        in_files.append(dest)
    else:
        write_log("Error::Input Missing[{}]".format(os.path.basename(f)))
        print("Error::Input Missing[{}]".format(os.path.basename(f)))

print ("{} files in temp input".format(str(len(in_files)) ) ) #debug for filecount