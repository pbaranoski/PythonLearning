#!/usr/bin/env python
########################################################################################################
# Name:  SQLSnowFlakeFncts.py
#
# Desc: Common module with Snowflake DB functions.
#        NOTE: Import module into Python program to use functions.
#
# Created: Paul Baranoski 03/18/2025
# Modified:
#
# Paul Baranoski 2025-03-18 Create Module.
########################################################################################################

import os
import csv
import logging

import sys
import datetime
from datetime import datetime
import sendEmail

import snowflake.connector
import json

class NullConnectException(Exception):
    "Connection object is null"

class NullCursorException(Exception):
    "Cursor object is null"

class ConfigFileNotfnd(Exception):
    "Configuration file not found: "
    
########################################################################################################
# Get directories and build path.
########################################################################################################
currentDirectory = os.path.dirname(os.path.realpath(__file__))
rootDirectory = os.path.abspath(os.path.join(currentDirectory, ".."))
utilDirectory = os.getenv('CMN_UTIL')

sys.path.append(rootDirectory)
sys.path.append(utilDirectory)
script_name = os.path.basename(__file__)


###############################
# Functions
###############################
def closeConnection(cnx):

    print("start function closeConnection()")

    if cnx is not None:
        cnx.close()


def getSFCredentials():

    print("start function getSFCredentials()")
    
    # Get location of SF credentials file
    logonDirectory=os.path.dirname(r"/app/IDRC/XTR/CMS/scripts/logon/")
    SFCredentialsFile=os.path.join(logonDirectory, "sf.logon")

    try:     
        
        with open(SFCredentialsFile, "r") as sfCredFile:
            sfCredDict = json.load(sfCredFile)
            ##print(f"{sfCredDict=}")
            print("Sucessfully read SF logon file")
            
        # return dictionary with SF credentials and connection information    
        return sfCredDict    
        
    except Exception as e:
       print(e)
       raise
                   

def getConnection():

    #logger.debug("start function getConnection()")
    print("start function getConnection()")
    
    cnx = None

    try: 

        ###################################################
        # Get Snowflake credentials
        ###################################################     
        sfCredDict = getSFCredentials()

        ###################################################
        # Connect to Snowflake
        ###################################################     
        con = snowflake.connector.connect(user=sfCredDict['SNOW_USER'], password=sfCredDict['SNOW_PASSWORD'], 
            account=sfCredDict['SNOW_ACCOUNT'], 
            warehouse=sfCredDict['SNOW_WAREHOUSE'], database=sfCredDict['SNOW_DATABASE'])        

        #logger.info("Connected to Database!")
        #logger.debug(getDriverVersion(con))
        print("Connected to Database!")
        
        return con

    except Exception as err:    
        #logger.error("Could NOT connect to Database!")
        #logger.error(err)
        print("Could NOT connect to Database!")
        print(err)
        
        raise


def getAllRows(sqlStmt, tupParms):
    ########################################################
    # function parms: 
    #   1) SQL string w/parm markers/or no parms
    #   2) tuple list of parms for SQL string (can be null). 
    #########################################################
    #logger.info("start function getAllRows()")
    
    print("start function getAllRows()")
    print(f"{sqlStmt=}")

    try:

        cnx = getConnection()

        curs = cnx.cursor()

        #loadCursorColumnList(cursor.description) 
        curs.description
        curs.rowcount
        curs._total_rowcount
        
   
        # parameters must be a tuple
        #if tupParms is None:
        #    cursor = cnx.execute_string(sqlStmt)
        #else:
        #    cursor = cnx.execute_string(sqlStmt)

        if curs is None:
            raise NullCursorException() 

        for row in curs:
            print(row) 
                
            #records += row

        # create list of column names
        #loadCursorColumnList(cursor.description)
        #logger.debug("cursor columns: "+ str(cursor.description))
        #print("cursor columns: "+ str(cursor.description))
        #print(f"{records=}")

        #return records

    except Exception as e:
        print("Error with Select: "+sqlStmt) 
        print(e)
        raise
    
    finally: 
        if cnx is not None:
            #if cursor is not None:
            #    cursor.close()
            cnx.close()    

            
# Execute getConnection function        
getConnection()        

getAllRows("SELECT '5' FROM DUAL;", None)
 

