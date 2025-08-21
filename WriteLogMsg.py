import os
import sys
import datetime

log_dir = "C:\\Users\\user\\Documents\\PythonLearning\\logs"


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
    # Its easier for others to understand your code if you parse out the input variable first
    # then build the error message.  The geocode program mixes them.

    # parse out input into variables
    # "Error::Skipped[filename.csv]"
    msgarr = msg.split("::")
    print ("msgarr: "+str([m for m in msgarr]))
    print ("msgarr len: "+str(len(msgarr)) )
    
    # arrays are zero-based
    print ("msgarr[0]: "+msgarr[0])
    print ("msgarr[1]: "+msgarr[1])
    
    # find position of character "[" in string variable
    print ("pos of `[` zero-based"+str(msgarr[1].find("[")))
    print ("display only 1st 7 characters for 2nd array item: "+msgarr[1][:7])

    # substrings --> The colon is key in the brackets
    status= msgarr[1][:msgarr[1].find("[")]

    # 2nd brakets are substring argument 
    # positive number before colon is Start position (like java)
    # positive number after colon are the num of chars to display; ending-offset (not inclusive - like java)
    # startPos = msgarr[1].find("[")+1 
    # endPos =  msgarr[1].find("]")
    print("TEST \/\/\/\/")
    print (msgarr[1])
    print(msgarr[1].find("[")+1)
    print (msgarr[1].find("]"))
    print (msgarr[1][8:19])
    file_name = msgarr[1][msgarr[1].find("[")+1 : msgarr[1].find("]")]


    print ("file_name: "+file_name)
    print("TEST \/\/\/\/")
    
    log_details = []
    date = datetime.datetime.now()
    time_stamp = date.strftime("%m/%d/%Y %H:%M:%S")
    log_details.append(time_stamp)
    log_details.append(status)
    log_details.append(file_name)

    # display detail msg for msg_Category (Skipped, Failed, etc)
    status_msg = status_details.get(status)
    # If length > 2; then status_msg was supplied, so use that instead of the value
    # from the look-up table (code line above this comment). 
    # Including an ELSE with the above code line would have made this more obvious. 
    if len(msgarr) > 2:
        status_msg = status_msg.format(str(msgarr[2]))

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

csv_name = "C:/Users/user/Documents/PythonLearning/LandingDir/InfolderPath/csvlist.txt"

write_log("Error::Skipped[{}]".format(os.path.basename(csv_name)))
