#!/usr/bin/python3
#-----------------------------------------------------------------------------#
# Date  : 2021-12-28
# Auth  : Paul Baranoski
# Test Python script to print the current working directory
#  and the sub-directories
#

import sys
import os
import datetime
import logging


#print(type(os.environ))
#print(isinstance(os.environ, dict))
#os.environ.get('HOME')
#for key in os.environ:
#   print(str(key))
#    #print (value)


#TstDate = '2022-10-01'
#print(TstDate[0:7].replace("-",""))


filenameAndPath = os.path.join(os.getcwd(), "pwdPrintTest.py")
print(os.path.dirname(filenameAndPath))
print(os.path.basename(filenameAndPath))
print(os.path.split(filenameAndPath))
print(os.path.exists(filenameAndPath))

print(os.path.isdir(filenameAndPath))
print(os.path.isfile(filenameAndPath))

print("extension and Drive Letter")
# tuple: with extension as 2nd member
print(os.path.splitext(filenameAndPath))
# tuple: where drive letter C: is separate from rest of filename
print(os.path.splitdrive(filenameAndPath))


if __name__ == "__main__":

    ###################################################
    # Set log directory and filename
    ###################################################
    curDir = os.getcwd()
    #parentDir = os.path.abspath(os.path.join(curDir, os.pardir))
    parentDir = curDir
    logsDir = os.path.join(parentDir,"logs")
    logfileName = "pwdPrintTestLog_"+ datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logfile  = os.path.join(logsDir, logfileName)

    ###################################################
    # configure logger
    ###################################################
    logging.basicConfig(
        #format="%(asctime)s %(levelname)-8s %(threadName)s %(funcName)s %(message)s", #--> %(name)s give logger name
        format="%(asctime)s %(levelname)-8s %(funcName)-12s %(message)s",
        encoding='utf-8',
        datefmt="%Y-%m-%d %H:%M:%S", 
        #filename=logfile, 
        handlers=[
        logging.FileHandler(logfile),
#        logging.StreamHandler(sys.stdout)
        ],
        level=logging.INFO)

    logger = logging.getLogger(__name__) 


    ###################################################
    # Create some log messages
    ###################################################
    logger.info("########")
    logger.info("Start of script")

    logger.info("LogfileName: "+logfileName)
    logger.info("pwd: "+os.getcwd())
    logger.info("parent Dir:" + parentDir)

    ###################################################
    # iterate of sub-directories
    ###################################################
    projDirBaseList = (dirItem for dirItem in os.listdir(curDir) if os.path.isdir(os.path.join(curDir,dirItem)) )

    for projDirBase in projDirBaseList:
        logger.info ("subdir: "+projDirBase)
        projDirPath = os.path.join(curDir,projDirBase)
        logger.info("fullpath: "+projDirPath)


