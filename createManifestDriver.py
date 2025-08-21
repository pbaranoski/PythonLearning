#!/usr/bin/env python
############################################################################################################
# Name:  CreateManifestFileDriver.py
#
# Desc: Create Manifest file required for transfers of Extract files to Outside Consumers using BOX 
#
# Execute as python3 CreateManifestFileDriver.py --bucket {parm1} --folder {parm2} --runToken {parm3} --BoxEmails {parm4} --Manifest_folder {parm5} --Ext_Type {parm6}
#
# parm1 = S3 bucket where extract files live.       Ex1: bucket=aws-hhs-cms-eadg-bia-ddom-extracts-nonrpod  
#                                                   Ex2: bucket=aws-hhs-cms-eadg-bia-ddom-extracts
# parm2 = S3 folder name where extract files live.  Ex1: xtr/DEV/Blbtn/  
#                                                   Ex2: xtr/Blbtn/
# parm3 = S3 filename timestamp  Ex:  20220922.084321   
# parm4 = Box account email addresses (comma delimited string)  
# parm5 = (optional) Destination manifest_files folder (DEFAULT=Manifest_files, SSA_BOX, VA_BOX) 
# parm6 = (optional) Key to use against JIRA_Extract_Mappings.txt to find JIRA ticket # for manifest file. When Key cannot be determined by S3 folder like SSA_BOX. 
#
#
# 07/28/2025 Paul Baranoski   Created script.	
############################################################################################################
import logging
import sys
import argparse

import json

#import datetime
from datetime import datetime
from datetime import date,timedelta

import os
import subprocess


#############################################################
# Functions
#############################################################
def setLogging(LOGNAME):

    # Configure root logger
    #logging.config.fileConfig(os.path.join(config_dir,"loggerConfig.cfg"))
    
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(funcName)-22s %(message)s",
        encoding='utf-8', datefmt="%Y-%m-%d %H:%M:%S", 
        #filename=f"{LOG_DIR}BuildRunExtCalendar_{TMSTMP}.log"
        handlers=[
        logging.FileHandler(f"{LOGNAME}"),
        logging.StreamHandler(sys.stdout)],    
        level=logging.INFO)
 
    global rootLogger
    rootLogger = logging.getLogger() 
  
      
def main_processing_loop():

    try:    

        ##########################################
        # Set Timestamp for log file and extract filenames
        ##########################################
        global TMSTMP
        global LOGNAME


        #TMSTMP = If TMSTMP value set by caller via export --> use that value. 
        #         Else use the timestamp created in this script        
        try:
            TMSTMP = os.environ["TMSTMP"]

        except KeyError:
            # if environment variable doesn't exist --> create it.
            TMSTMP = datetime.now().strftime('%Y%m%d.%H%M%S')
            os.environ["TMSTMP"] = TMSTMP        
        
        print(f"{TMSTMP=}")

        LOGNAME = f"CreateManifestFile_{TMSTMP}.log"
        
        ##########################################
        # Establish log file
        # NOTE: the \n before "started at" line is to ensure that this information is on a separate line, left-justified without any other logging info preceding it        
        ##########################################
        setLogging(LOGNAME)

        rootLogger.info("################################### ")
        rootLogger.info(f"\nCreateManifestFileDriver.py started at {TMSTMP} ")

        ###########################################################
        # Set working directory to scripts/run directory.
        # This is so subprocess calls will work from RunDeck.  
        ###########################################################
        pwd = os.getcwd()
        rootLogger.info(f"{pwd=}")

 
        #######################################################
        # Get parameters.
        # Caller passes None for parameter overrides
        #######################################################
        parser = argparse.ArgumentParser(description="Create ManifestFile Driver")
        parser.add_argument("--bucket", help="S3 bucket")
        parser.add_argument("--folder", help="S3 folder")
        parser.add_argument("--runToken", help="Run Token timestamp")
        parser.add_argument("--BoxEmails", help="Box account email addresses")
        parser.add_argument("--Manifest_folder", required=False, default=None, help="manifest folder Override")
        parser.add_argument("--Ext_Type", required=False, default=None, help="Extract Type Override")

        args = parser.parse_args()

        #############################################################
        # Display parameters passed to script 
        # Ex. CreateManifestFile.sh --bucket {s3 Bucket} --folder xtr/DOJ/ --runToken "20231211.125522" --BoxEmails "pbaranoski-con@index.com" 
        #############################################################
        rootLogger.info(f"Parameters sent to script. ")  
        rootLogger.info("args:")    
        rootLogger.info(f"{args.bucket=}")
        rootLogger.info(f"{args.folder=}")
        rootLogger.info(f"{args.runToken=}")
        rootLogger.info(f"{args.BoxEmails=}")
        
        #############################################################
        # Assign parameters to variables 
        #############################################################
        S3Bucket = args.bucket
        S3BucketFldr = args.folder
        S3FilenameTmstmp = args.runToken
        RecipientEmails = args.BoxEmails
       


    except Exception as e:
        print (f"Exception occured in CreateManifestFileDriver.py\n {e}")

        rootLogger.error("Exception occured in CreateManifestFileDriver.py.")
        rootLogger.error(e)

        sys.exit(12)    

def createManifestFile(bucket="XTR_Bucket", folder="default_Fldr", runToken='20250101.120101', BoxEmails=None, Manifest_folder=None, Ext_Type=None ):

    ##########################################
    # Set Timestamp for log file and extract filenames
    ##########################################
    global TMSTMP
    global LOGNAME


    #TMSTMP = If TMSTMP value set by caller via export --> use that value. 
    #         Else use the timestamp created in this script        
    try:
        TMSTMP = os.environ["TMSTMP"]

    except KeyError:
        # if environment variable doesn't exist --> create it.
        TMSTMP = datetime.now().strftime('%Y%m%d.%H%M%S')
        os.environ["TMSTMP"] = TMSTMP        
    
    print(f"{TMSTMP=}")

    LOGNAME = f"CreateManifestFile_{TMSTMP}.log"
    
    ##########################################
    # Establish log file
    # NOTE: the \n before "started at" line is to ensure that this information is on a separate line, left-justified without any other logging info preceding it        
    ##########################################
    setLogging(LOGNAME)

    rootLogger.info("################################### ")
    rootLogger.info(f"\nCreateManifestFileDriver.py started at {TMSTMP} ")

    ###########################################################
    # Set working directory to scripts/run directory.
    # This is so subprocess calls will work from RunDeck.  
    ###########################################################
    pwd = os.getcwd()
    rootLogger.info(f"{pwd=}")

    rootLogger.info(f"{bucket=} ")  
    rootLogger.info(f"{folder=} ")  
    rootLogger.info(f"{runToken=} ")  
    rootLogger.info(f"{BoxEmails} ")  

    return 88


if __name__ == "__main__":
    
    main_processing_loop()