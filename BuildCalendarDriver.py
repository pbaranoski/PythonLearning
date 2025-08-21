#!/usr/bin/env python

import os
import logging
import sys
import re
import argparse

#import datetime
from datetime import datetime
from datetime import date,timedelta

#############################################################
# Constants
#############################################################
# M-F
WORKING_DAYS_MASK="12345"
FLD_DELIM="|"

MON_ABREVS="JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC"
MON_ABREVS_DELIM="JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC"

DAYS4MM_NON_LEAP_YR="31|28|31|30|31|30|31|31|30|31|30|31"
DAYS4MM_LEAP_YR="31|29|31|30|31|30|31|31|30|31|30|31"
#DAYS4MM=""
VALID_DOM_LF_VALUES="LWFWLDFD"

CONFIG_INPUT_FILE=r"C:\Users\PaulBaranoski\OneDrive - Index Analytics\Documents\Sprints\CalendarCreate\CalendarConfigFile.csv"

ValidNumeredDay = '^[0-9]+$'
ValidDayAbrevAndOcc = '^(SUN|MON|TUE|WED|THU|FRI|SAT)-(1|2|3|4|L|F)$'
ValidLWFWLDFD = '^(LW|FW|LD|FD)$'
		

def getMatchingDOWDate(parmStartDt, parmDOWMask, parmOcc, parmSign):

	#################################################################################################################	
	# This function will find the 1st, 2nd, 3rd, last Day-of-week (FRI, MON, etc) and set that as the return date.
	# parmStartDt =  (YYYY-MM-01 format) or (YYYY-MM-31 - last day of month) 
	# parmDOWMask = 0-6 reprsenting the day(s) of the week like 5=Fri. "12345" -> every work day; "15" --> Mon and Fri' 
	#           "5" --> Friday
	# parmOcc = 1,2,3 (1st, 2nd, 3rd); 'FW' or 'FD' --> parmOCC = '1' (sign=+); 'LW' or 'LD' --> parmOCC = '1' (sign=-)
	# parmSign = '+' or '-'
	#
	#################################################################################################################	
	
    rootLogger.info(f"{parmStartDt=} ") 
    rootLogger.info(f"{parmDOWMask=} ") 
    rootLogger.info(f"{parmOcc=} ") 
    rootLogger.info(f"{parmSign=} ") 
	
	###########################################################
	# if parmStartDt the search dow? (like Fri) --> skip loop
	# if not dow looking for --> find 
	###########################################################
    NOF_Occ=0

    rootLogger.info("starting loop ") 

    for days_sub in range(0, 31):

        # convert parmStartDt to datetime object
        dttmStartDt = datetime.strptime(parmStartDt,'%Y-%m-%d')

        NOF_DAYS = int(parmSign + str(days_sub) )
        rootLogger.info(f"{NOF_DAYS=}")  

        # Calculate new date
        dttmCalcDate = (dttmStartDt + timedelta(days=NOF_DAYS))
        sCalcDate_YYYYMMDD = dttmCalcDate.strftime('%Y-%m-%d')
        # 0-6 Sun-Sat
        dow_nbr = dttmCalcDate.strftime('%w')

        rootLogger.info(f"{sCalcDate_YYYYMMDD=}")  
        rootLogger.info(f"{dow_nbr=}")  

		# is the date dow = requested DOW?
        MatchIdx = parmDOWMask.find(dow_nbr)
        rootLogger.info(f"{MatchIdx=}")  

		# date dow = requested DOW
        if  MatchIdx != -1:
            NOF_Occ+=1  

            rootLogger.info(f"{NOF_Occ=}")   

            if NOF_Occ == int(parmOcc):
                rootLogger.info("NOF OCC criteria met")    

                # criteria satisfied
                break
    
    return sCalcDate_YYYYMMDD


def getDaysMatchMask(DOW_parm):

    # initialize match Mask
    global REQ_DAYS_MASK 
    REQ_DAYS_MASK = ""

    if DOW_parm == "M-F":
        REQ_DAYS_MASK=WORKING_DAYS_MASK	
    else:
		# parse days by delimiter (,)
		# MON,TUE,WED,THU,FRI,SAT,SUT
		
        DAYS_ARRAY = DOW_parm.split(",")
        rootLogger.info(f"{len(DAYS_ARRAY)=} ") 
        rootLogger.info(f"{DAYS_ARRAY=} ") 

		# Build Days Mask
        for DAY in DAYS_ARRAY:
            rootLogger.info(f"{DAY=} ") 

			# convert Days array to use 3-char day names
            if DAY == "MON":
                REQ_DAYS_MASK=REQ_DAYS_MASK + "1"
            elif DAY ==	"TUE":	
                REQ_DAYS_MASK=REQ_DAYS_MASK + "2"				
            elif DAY ==	"WED":	
                REQ_DAYS_MASK=REQ_DAYS_MASK + "3"				
            elif DAY ==	"THU":	
                REQ_DAYS_MASK=REQ_DAYS_MASK + "4"				
            elif DAY ==	"FRI":	
                REQ_DAYS_MASK=REQ_DAYS_MASK + "5"				
            elif DAY ==	"SAT":	
                REQ_DAYS_MASK=REQ_DAYS_MASK + "6"				
            elif DAY ==	"SUN":	
                REQ_DAYS_MASK=REQ_DAYS_MASK + "0"				

    rootLogger.info(f"{REQ_DAYS_MASK=} ") 

    return REQ_DAYS_MASK
	

def getMonthNumber(p_searchMon: str): 
	
    searchMon = p_searchMon.upper()
    rootLogger.info(f"Search Month parameter {p_searchMon} was upper-cased to {searchMon}.")

    idx = MON_ABREVS.find(searchMon)
    if idx == -1:
        rootLogger.error(f"Search Month parameter {p_searchMon} is not a valid month.")
        sys.exit(12)


    rootLogger.info(f"{searchMon} was found at {idx=}")

    monthNbr = int((idx / 3) + 1)
    rootLogger.info(f"{monthNbr=}")

    MMFormatted = "{:02d}".format(monthNbr)
    rootLogger.info(f"{MMFormatted=}")

    return MMFormatted


def setNOFDaysForYear(sYYYY):

    import calendar

    global DAYS4MM     

    if calendar.isleap(int(sYYYY)):
        NOF_Days_in_Year = 366
        DAYS4MM=DAYS4MM_LEAP_YR
    else:    
        NOF_Days_in_Year = 365
        DAYS4MM=DAYS4MM_NON_LEAP_YR

    rootLogger.info(f"{NOF_Days_in_Year=}")
    rootLogger.info(f"{DAYS4MM=}")

    return NOF_Days_in_Year


def setLogging():

    # Configure root logger
    #logging.config.fileConfig(os.path.join(config_dir,"loggerConfig.cfg"))
    
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(funcName)-22s %(message)s",
        encoding='utf-8', datefmt="%Y-%m-%d %H:%M:%S", 
        handlers=[
        logging.FileHandler(f"BuildRunExtCalendar_{TMSTMP}.log"),
        logging.StreamHandler(sys.stdout)],    
        level=logging.DEBUG)
 
    global rootLogger
    rootLogger = logging.getLogger() 


def buildWkCal4Yr(fCalendarFile, p_out_rec):

    rootLogger.info(f"{p_out_rec=} ")      

    # Set date to first day of year
    sStartDate = sProcessingYYYY + "-01-01"
    dttmStartDt = datetime.strptime(sStartDate,'%Y-%m-%d')
    rootLogger.info(f"{sStartDate=} ")   

 
	# loop thru days of year to create appropriate calendar records
    for iDays in range(0, 365):

        # Calculate new date
        dttmCalcDate = (dttmStartDt + timedelta(days=iDays))
        sNextDt = dttmCalcDate.strftime('%Y-%m-%d')
        rootLogger.info(f"{sNextDt=} ") 

		# skip if year is not for current processing year
        if sNextDt[:4] != sProcessingYYYY:
            break
		
		# get day of week
        dow_nbr = dttmCalcDate.strftime('%w')    
        rootLogger.info(f"{dow_nbr=} ") 


		# if day of week we need --> create date
        if REQ_DAYS_MASK.find(dow_nbr) != -1: 
		########################################################
		# Build Calendar record --> append calendar info to 
		#                           config record
		########################################################	
            sDOWAbbrev = dttmCalcDate.strftime('%a')   
            sExtDt = sNextDt 

            rootLogger.info(f"This date matches criteria: {sExtDt=} ")  
            rootLogger.info(f"This date matches criteria: {sDOWAbbrev=} ")  
			
			# output record and add Extract day and NOD
            sCalendarOutputRec = sExtDt + FLD_DELIM + sDOWAbbrev + FLD_DELIM + p_out_rec
            fCalendarFile.write(sCalendarOutputRec)


def buildQtrCal4Yr(fCalendarFile, p_Months, p_Month_Day, p_out_rec):

    ###################################################
    # p_Months like: "JAN,APR,JUL,OCT" or "JAN,JUL"
    # p_Month_Day: 2-digit day number 
    #             LW,FW,LD,FD,
    #             "FRI-2" (2nd FRI) "FRI-L" (last FRI)
    #             "FRI-F" (first FRI)
    ###################################################
    rootLogger.info(f"{p_Months=} ")
    rootLogger.info(f"{p_Month_Day=} ")
    rootLogger.info(f"{p_out_rec=} ")     

    ###################################################	
    # Local variables 
    ###################################################		
    sQtrDate = ""

    ###################################################	
    # Validate Month_Day
    # valid values --> month number (DD)
    #                 (LW|FW|FD|LD) 
    #                 (FRI-2|FRI-L) etc.
    ###################################################
    reValidNumeredDay = re.compile(ValidNumeredDay)
    reValidDayAbrevAndOcc = re.compile(ValidDayAbrevAndOcc, re.IGNORECASE)
    reValidLWFWLDFD = re.compile(ValidLWFWLDFD, re.IGNORECASE)

	
    if reValidNumeredDay.match(p_Month_Day):
        rootLogger.info(f"Valid month number {p_Month_Day} ")   
		 
    elif reValidDayAbrevAndOcc.match(p_Month_Day):
        rootLogger.info(f"Valid Day and Occurrence - Ex. FRI-2 --> {p_Month_Day} ") 
		
    elif reValidLWFWLDFD.match(p_Month_Day):
        rootLogger.info(f"Valid value (LW|FW|FD|LD) --> {p_Month_Day} ") 

    else:
        rootLogger.info(f"Invalid DOM value {p_Month_Day} in config file record {p_out_rec} ") 	
	
        # Send Failure email	
        #SUBJECT=f"BuildRunExtCalendar.sh  - Failed ({ENVNAME})"
        #MSG=f"Invalid DOM value {p_Month_Day} in config file record {p_out_rec}. Process failed. "
        # ${RUNDIR}sendEmail.py "${CMS_EMAIL_SENDER}" "${ENIGMA_EMAIL_FAILURE_RECIPIENT}" "${SUBJECT}" "${MSG}" >> ${LOGNAME} 2>&1

        sys.exit(12)


	###################################################	
	# Convert Months comma-delimited string to space-delimited
	# Ex. "JAN,APR,JUL,OCT" --> "JAN APR JUL OCT"
	###################################################
    lsMonthsArray=p_Months.split(",")
    rootLogger.info(f"{lsMonthsArray=} ")  
    rootLogger.info(f"Number of elements in the array: {len(lsMonthsArray)=} ")	
	
	###################################################	
	# Loop thru Months array
	###################################################
    for sMON in lsMonthsArray:
        rootLogger.info("*------------------------------*") 
        rootLogger.info(f"{sMON=}") 

		# Convert Month abbrev to month number
        sMMFormatted = getMonthNumber(sMON)
        rootLogger.info(f"{sMMFormatted=}") 

		#################################################
		# Build date using Month number and month day
		# or Get appropriate date
		# --> Format date in YYYY-MM-DD format
		#################################################
		# last working day for month
        if  p_Month_Day == "LW":

            idx = int(sMMFormatted) - 1
            dd = DAYS4MM.split("|") [idx]

            rootLogger.info(f"{dd=}")
			
            parmStartDt = f"{sProcessingYYYY}-{sMMFormatted}-{dd}"
            parmDOWMask = WORKING_DAYS_MASK
            parmOcc = 1
            parmSign = "-"
				
            sQtrDate = getMatchingDOWDate (parmStartDt, parmDOWMask, parmOcc, parmSign)

        elif  p_Month_Day == "FW":		
			# first working day for month

            parmStartDt = f"{sProcessingYYYY}-{sMMFormatted}-01"
            parmDOWMask = WORKING_DAYS_MASK
            parmOcc = 1
            parmSign = "+"

            sQtrDate = getMatchingDOWDate (parmStartDt, parmDOWMask, parmOcc, parmSign)
            rootLogger.info(f"{sQtrDate=}")         

        elif p_Month_Day == "LD": 	
			# find last day for month

            idx = int(sMMFormatted) - 1
            dd = DAYS4MM.split("|") [idx]
            rootLogger.info(f"{dd=}")
			
			# Set Extract date variable	
            sQtrDate=f"{sProcessingYYYY}-{sMMFormatted}-{dd}"

        elif p_Month_Day == "FD":				
			# find first day for month
            sQtrDate=f"{sProcessingYYYY}-{sMMFormatted}-01"

        elif  reValidDayAbrevAndOcc.match(p_Month_Day):
			# Ex. (FRI-2) --> 2nd FRI of month 
			
			# separate DOW_DAY from modifier
            lsDayAbrevAndOcc = p_Month_Day.split("-")
            # SUN,MON, FRI etc.
            DOW_DAY = lsDayAbrevAndOcc[0]
            # [1234LW]
            DOW_MODIFIER = lsDayAbrevAndOcc[1]

            rootLogger.info(f"{DOW_DAY=}")			
            rootLogger.info(f"{DOW_MODIFIER=}")			

			# Build DOW mask
            sDOWMask = getDaysMatchMask(DOW_DAY)
            parmDOWMask = sDOWMask
			
			# Set parms for function
            if DOW_MODIFIER == "L":

                dd = DAYS4MM.split("|") [int(sMMFormatted - 1)]
                rootLogger.info(f"{dd=}")
			
                parmStartDt = f"{sProcessingYYYY}-{sMMFormatted}-{dd}"
                parmOcc= "1"			
                parmSign = "-"

            elif DOW_MODIFIER == "F": 
                parmStartDt = f"{sProcessingYYYY}-{sMMFormatted}-01"
                parmOcc = "1"	
                parmSign = "+"				
			
            else:
                parmStartDt = f"{sProcessingYYYY}-{sMMFormatted}-01"
                parmOcc = DOW_MODIFIER 
                parmSign = "+"

			# Get matching DOW	
            sQtrDate = getMatchingDOWDate (parmStartDt, parmDOWMask, parmOcc, parmSign) 
			
        else:
			# p_Month_Day is number 

			# !!!!If p_Month_Day is > NOF days per month --> substitute correct NOF days per month
            idx = int(sMMFormatted) - 1
            dd = DAYS4MM.split("|") [idx]
            rootLogger.info(f"{dd=}")

            if p_Month_Day > dd: 
                parmStartDt=f"{sProcessingYYYY}-{sMMFormatted}-{dd}"
            else:
                parmStartDt=f"{sProcessingYYYY}-{sMMFormatted}-{p_Month_Day}"
			
			# find nearest prior working day for config day
            parmDOWMask = WORKING_DAYS_MASK
            parmOcc = "1"
            parmSign = "-"
				
            sQtrDate = getMatchingDOWDate (parmStartDt, parmDOWMask, parmOcc, parmSign)


        rootLogger.info(f"{sQtrDate=}")

		#################################################
		# Build output record	
		#################################################		
        dttmQtrDt = datetime.strptime(sQtrDate,'%Y-%m-%d')	
        sDOWAbbrev = dttmQtrDt.strftime('%a')   

        # output record and add Extract day and NOD
        sCalendarOutputRec = sQtrDate + FLD_DELIM + sDOWAbbrev + FLD_DELIM + p_out_rec
        fCalendarFile.write(sCalendarOutputRec)		


def main_processing_loop():

    try:    

        # Set Timestamp for log file and extract filenames
        global TMSTMP
        TMSTMP = datetime.now().strftime('%Y%m%d.%H%M%S')
        print(f"{TMSTMP=}")

        ##########################################
        #  Establish log file
        ##########################################
        setLogging()
        rootLogger.info("Start Build Calendar Driver python module ")

        ##########################################
        #  Establish global variables
        ##########################################
        sConfigRec = ""

        global sProcessingYYYY 
        sProcessingYYYY="2025"

        ##########################################
        # Get any parameters
        ##########################################
        #parser = argparse.ArgumentParser(description="BuildCalDriver parms")
        #parser.add_argument("--ProcessingYear", help="Year to create calendar for: YYYY")
        #args = parser.parse_args()

        #sProcessingYYYY=str(args.ProcessingYear)


        # Accept override parameter
        setNOFDaysForYear(sProcessingYYYY)

        global CALENDAR_OUTPUT_FILE
        CALENDAR_OUTPUT_FILE=fr"C:\Users\PaulBaranoski\OneDrive - Index Analytics\Documents\Sprints\CalendarCreate\RunCalendar_{sProcessingYYYY}.txt"

        ##########################################
        # main processing
        ##########################################
        rootLogger.info("Processing Configuration File") 

        with open(CONFIG_INPUT_FILE, 'r') as fConfigFile, open(CALENDAR_OUTPUT_FILE, 'w') as fCalendarFile:  
            for sConfigRec in fConfigFile:

                rootLogger.info("*****************************") 
                rootLogger.info("read next Config Record") 
                rootLogger.info(f"{sConfigRec=}")  
                lstConfigRecFlds = sConfigRec.split("|") 

                ####################################################
                # parse input record into separte fields by '|'
                # Example: Blbtn,Blue Button,W,M;F,,,N,EFT 
                ####################################################
                ExtractID = lstConfigRecFlds[0].strip() 
                Ext_Desc = lstConfigRecFlds[1].strip()
                TimeFrame = lstConfigRecFlds[2].strip()
                DOW_DOM = lstConfigRecFlds[3].strip()
                Months = lstConfigRecFlds[4].strip()
                Month_Day = lstConfigRecFlds[5].strip()
                FinderFileReq = lstConfigRecFlds[6].strip()
                FF_Pre_Processing = lstConfigRecFlds[7].strip()
                DeliveryMethod = lstConfigRecFlds[8].strip()

                rootLogger.info(f"{ExtractID=}")  	
                rootLogger.info(f"{Ext_Desc=}")  	
                rootLogger.info(f"{TimeFrame=}")        
                rootLogger.info(f"{DOW_DOM=}")        
                rootLogger.info(f"{Months=}")        
                rootLogger.info(f"{Month_Day=}")        
                rootLogger.info(f"{FinderFileReq=}")        
                rootLogger.info(f"{FF_Pre_Processing=}")        
                rootLogger.info(f"{DeliveryMethod=}")         

                ####################################################
                # Create year calendar records for extract
                ####################################################
                if TimeFrame == 'W':
                    rootLogger.info("Processing Weekly Extract")   

                    DaysMatchMask = getDaysMatchMask(DOW_DOM)
                    rootLogger.info(f"{DaysMatchMask=}")  
                    buildWkCal4Yr(fCalendarFile, sConfigRec) 

                elif TimeFrame == 'M':
                    rootLogger.info("Processing Monthly Extract")  
                    buildQtrCal4Yr(fCalendarFile, MON_ABREVS_DELIM, DOW_DOM, sConfigRec)
                    
                elif TimeFrame == 'Q' or TimeFrame == 'S' or TimeFrame == 'A':   
                    buildQtrCal4Yr(fCalendarFile, Months, Month_Day, sConfigRec)

                else:
                    rootLogger.info(f"Invalid extract time frame: {TimeFrame} in config file record {sConfigRec}") 	
                
                    ## Send Failure email	
                    #SUBJECT="BuildRunExtCalendar.sh  - Failed (${ENVNAME})"
                    #MSG="Invalid extract time frame: ${TimeFrame} in config file record ${config_rec}. Process failed. "
                    #${PYTHON_COMMAND} ${RUNDIR}sendEmail.py "${CMS_EMAIL_SENDER}" "${ENIGMA_EMAIL_FAILURE_RECIPIENT}" "${SUBJECT}" "${MSG}" >> ${LOGNAME} 2>&1

                    sys.exit(12)	

                # Accept parmeter for Year  
                # Create SET_XTR_ENV.py for DATA_DIR - 
                # Open an S3 file (config); write contents to S3 file directly.
                # Move and copy S3 files > 5GB		


        rootLogger.info("All Records processed in Configuration File") 

        #MM_Number = getMonthNumber("sep")
        #rootLogger.info(f"{MM_Number=}")    

        #DaysMatchMask = getDaysMatchMask("MON,FRI")
        #rootLogger.info(f"{DaysMatchMask=}")  

        #buildWkCal4Yr(p_out_rec="")

        #sCalcDate_YYYYMMDD = getMatchingDOWDate(parmStartDt="2025-06-01", parmDOWMask="15",  parmOcc="1", parmSign="+")
        #rootLogger.info(f"{sCalcDate_YYYYMMDD=}")  

    except Exception as e:
        print (f"Exception occured in BuildCalendarDriver.py\n {e}")

        rootLogger.error("Exception occured in BuildCalendarDriver.py.")
        rootLogger.error(e)

        sys.exit(12)    

if __name__ == "__main__":
    
    main_processing_loop()