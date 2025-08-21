# python learning

import os
import sys
import time
#import optparse
import configparser

print ("arv0"+os.path.dirname(sys.argv[0]))

###############################
# os.path tests --> include variables in print output
###############################
print ("########--> OS.* test")

## C:/Users/user
print ("Our current working directory is " + os.getcwd())

# c:\Users\user\Documents\PythonLearning\PTest1.py
print ("Our script name is " + __file__)

## Change working directory to where script is running from
print("Script directory is "+os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))
print ("Our new current working directory is " + os.getcwd())

## change directory to config path
configPath = os.getcwd() + "\config"
print ("The config path is: " + configPath)
os.chdir(configPath) 
print ("Our current working directory is " + os.getcwd())

print ("")

###############################
# get values from config file
###############################
print ("##### --> Config File Test")

config = configparser.ConfigParser()
if os.path.exists(configPath+"\config.txt"):
    print("Path exists")
else:
    print ("Path does not exist")

config.read(configPath+"\config.txt")
print (config.sections())

inFolderPath = config.get('PathSect','inFolderPath')
outFolderPath = config.get('PathSect','outFolderPath')
homeDir = config.get('PathSect','home_dir')

filestamp = time.strftime('%Y-%m-%d')

print (inFolderPath)
print (outFolderPath)
print (homeDir)
print (filestamp)


if os.path.exists(inFolderPath):
    print ("inFolderPath " + inFolderPath + " exists")
else:
    print ("inFolderPath '" + inFolderPath + "' does not exist")

print ("")

##################################
# get path name parts; join paths
##################################
print ("##### --> Path Name Tests")

print ("inFolderPath: "+inFolderPath)
print ("dirname inFolderPath: " + os.path.dirname(inFolderPath))
print ("basename inFolderpath: " + os.path.basename(inFolderPath))
print ("")

print ("homeDir from config file: "+homeDir)
configPath2 = os.path.join(homeDir,"config")
print ("os.path.join HomeDir + config path: " + configPath2)

## cannot concatenate str and bool
print ("Is joined path a valid Dir? " + str(os.path.isdir(configPath2)))
print ("")

###############################
# write to a file
###############################
print ("######### --> Writing to a file")

#print ("print w/o new line ".format(nl="\n")) 
print ("print w/o new line ".format(nl=""))  # this didn't work; nl still appended at at of line
print (" this is line 1 \n now line 2 with same print function.")

os.chdir(outFolderPath)
print("pwd: "+os.getcwd())


f = open('outtest.txt','w')
f.write("Record 1"+ "\n")
f.write("Record 2"+ "\n")
f.close()

print ("")

###############################
# function File test
###############################
print ("######### --> Function file test")

dirname = homeDir
logDir = os.path.join(homeDir,"logs")
logFile = os.path.join(logDir,"log.txt")
print ("logFile: "+logFile)

if (os.path.exists(logDir)):
    print("logDir "+logDir +" exists")
else:
    print("logDir does not exist")

fLogFile = open(logFile,'w')

def fnPrint2Log (logMsg):
    fLogFile.write(logMsg+"\n")
    return   

fnPrint2Log("LogMsg1")
fnPrint2Log("LogMsg2")
fLogFile.close()


print("before reading Log messages")
r = open(logFile,'r')
if r.mode == 'r':
    print("file is in read mode")

record = r.read()
print("record: "+record)
#print("readline: "+str(r.readline()))    ## one record at a time
#print("readlines: "+str(r.readlines()))  ## read into an array all records

print ("")

###############################
# if fall thru test
###############################
print ("######### --> IF fall thru-test")

log_fields = "this is the error/msg record"
dirname = homeDir
logDir = os.path.join(homeDir,"logs")
error_file = os.path.join(logDir,"error.txt")
message_file = os.path.join(logDir,"message.txt")

msg = "Error"
if msg == "Error":
        if not os.path.exists(error_file):
            fobj = open(error_file,"w")
            fobj.write(",".join(log_fields)+"\n")
            fobj.close()
        fobj = open(error_file,"a")
        print ("reachable code")
elif msg == "Message":
    if not os.path.exists(message_file):
        fobj = open(message_file,"w")
        fobj.write(",".join(log_fields)+"\n")
        fobj.close()
    fobj = open(message_file,"a")
fobj.write(",".join(log_fields)+"\n")
fobj.close()

sys.exit(0)

print ("script name:", sys.argv[0])
parm1= ("")
parm2= ("")

if len(sys.argv) == 3:
    parm1 = sys.argv[1]
    parm2 = sys.argv[2]
elif len(sys.argv) == 2:
    parm1 = sys.argv[1]
else:
    print ("no Parms entered.")
        
print (parm1)
print (parm2)


