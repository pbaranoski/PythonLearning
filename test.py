import datetime
import sys
import gzip
import json
import os
import re

#import datetime
from datetime import datetime
from datetime import date,timedelta

import logging

from io import StringIO

import test2 as childTest

TMSTMP = datetime.now().strftime('%Y%m%d.%H%M%S')

def create_logger(name, log_file, level=logging.INFO):
    """Set up a logger that writes logs to a specified file."""
    # Create a file handler that logs messages to the specified file
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')


    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logname = os.path.basename(f"/app/IDRC/XTR/CMS/logs/FOIA_MulticareDryer_Ext_{TMSTMP}.log").replace(f"_{TMSTMP}.log","")
    #logname.replace(f"_{TMSTMP}.log","")

    print(logname)
    logger = logging.getLogger("parent")
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    return logger

## Setting up the first logger for the first log file
first_logger = create_logger('parent', 'AParent.log')
first_logger.info('Logging to the parent log file as an info message.')

childTest.main_processing()

sys.exit(0)


def setLogging():

    #global TMSTMP
    TMSTMP = datetime.now().strftime('%Y%m%d.%H%M%S')
    print(f"{TMSTMP=}")

    # Configure root logger
    #logging.config.fileConfig(os.path.join(config_dir,"loggerConfig.cfg"))
    
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(funcName)-22s %(message)s",
        encoding='utf-8', datefmt="%Y-%m-%d %H:%M:%S", 
        filename=f"PSPS_SF_Table_Load_{TMSTMP}.log",
        #handlers=[
        #logging.FileHandler(f"PSPS_SF_Table_Load_{TMSTMP}.log"),
        #logging.StreamHandler(sys.stdout)],    
        level=logging.INFO)

    global rootLogger
    rootLogger = logging.getLogger() 
  
    #os.chmod(LOG_DIR, 0o777)  # for Python3
    
    #logger.setLevel(logging.INFO)


setLogging()

rootLogger.info("Hi there")

sys.exit(0)


def build_week_dt_parms(): 

    global wkly_strt_dt
    global wkly_end_dt

    # get (current date - 14 days) 
    dttmCalcDate = (datetime.today() + timedelta(days=-14))
    # get dow: Monday, Tuesday, etc.
    dow = dttmCalcDate.strftime('%A')
    wkly_strt_dt = dttmCalcDate.strftime('%Y-%m-%d')    

    # if current date is Monday --> skip loop
    # if not Monday --> find Monday prior to today )

    while dow != "Monday":

        dttmCalcDate = (dttmCalcDate + timedelta(days=-1))
        # get dow: Monday, Tuesday, etc.
        dow = dttmCalcDate.strftime('%A')
        wkly_strt_dt = dttmCalcDate.strftime('%Y-%m-%d')  
        print(f"{dow=}") 
        print(f"{wkly_strt_dt=}") 	   


    dttmCalcEndDate = (dttmCalcDate + timedelta(days=6))
    wkly_end_dt = dttmCalcEndDate.strftime('%Y-%m-%d')
    print(f"{wkly_end_dt=}")
 

def main_processing_loop():

    global wkly_strt_dt
    global wkly_end_dt

    iArg = 2
    if iArg ==  2:
        # Accept overrider parameter dates
        ParmOverrideFromDt = '2024-01-01'
        ParmOverrideToDt = '20204-01-07'
        wkly_strt_dt = ParmOverrideFromDt
        wkly_end_dt = ParmOverrideToDt 

        try:

            datetime_str = datetime.strptime("2025-02-29", "YYYY-MM-DD")

        except Exception as ex:
            print(ex)
            sys.exit(12)

        #except ValueError:
        #    print("Date is not in proper format")
        #    sys.exit(12)

    else:

        build_week_dt_parms()  


    print(f"{wkly_strt_dt=}")
    print(f"{wkly_end_dt=}")   



main_processing_loop()


sys.exit(0)


strLog = """
#     COPY INTO @BIA_DEV.CMS_STAGE_XTR_DEV
Before Executing SQL DUALS_MedAdv AH-AZ Extract
Executing: COPY INTO @BIA_DEV.CMS_STAGE_XTR_DEV.BIA_DEV_XTR_DUALS_MA_STG/DUALS_MedAdv_AH_AZ_202407_202409_20250128.085118.txt.gz
                                                FROM ( 

asdasdf                                              
asdf

Executing: COPY INTO @BIA_DEV.CMS_STAGE_XTR_DEV.BIA_DEV_XTR_DUALS_MA_STG/DUALS_MedAdv_AH_MD_202407_202409_20250128.085118.txt.gz
                                                FROM ( 

Query Start Time: 2025 01 28 08:53:12
Printing Result Set:
rows_unloaded,input_bytes,output_bytes
147148,13979060,181562

Query Start Time: 2025 01 28 08:53:12
Printing Result Set:
rows_unloaded,input_bytes,output_bytes
147149,13979061,181563

"""

print("In function getExtractFilenamesAndCounts()")

# Ex. "COPY INTO @BIA_DEV.CMS_STAGE_XTR_DEV.BIA_DEV_XTR_DUALS_MA_STG/DUALS_MedAdv_AH_MD_202407_202409_20250128.085118.txt.gz"
reCOPY_INTO_FILENAMES = re.compile('^Executing: COPY INTO @BIA_[a-zA-Z0-9_.]+[/]{1}[a-zA-Z0-9_.]+\.gz$', re.MULTILINE)
lstReResults = reCOPY_INTO_FILENAMES.findall(strLog)

# We want the 2nd part of the split command which is the extract filename
COPY_INTO_FILENAMES = [ extFilename.split("/")[1] for extFilename in lstReResults]
print("")
print(f"{COPY_INTO_FILENAMES=}")  


# Ex. 'rows_unloaded,input_bytes,output_bytes\n147148,13979060,181562' 
reRowsUnloaded = re.compile('^rows_unloaded,input_bytes,output_bytes\n[0-9]+,[0-9]+,[0-9]+', re.MULTILINE)
lstReResults = reRowsUnloaded.findall(strLog)
print("")
print(f"{lstReResults=}")

# Ex. '147148,13979060,181562' 
lstFileCounts = [EyeCatcherNCounts.split("\n")[1] for EyeCatcherNCounts in lstReResults]
ROW_INFO = lstFileCounts

# isolate the first number -> the record count from the three other counts (byte count,zipped byte count)
ROW_COUNTS = [fileCounts.split(",")[0]  for fileCounts in lstFileCounts]

print("")
print(f"{ROW_COUNTS=}")
print(f"{ROW_INFO=}")

lstFilenamesAndCounts = [f"{filename.ljust(50)} {int(count): >14,d}" for filename, count in zip (COPY_INTO_FILENAMES, ROW_COUNTS) ]
strFilenamesAndCounts = "\n".join(sFilenameAndCount for sFilenameAndCount in lstFilenamesAndCounts)  + "\n"

#strFilenamesAndCounts = "\n".join(FilenameAndCounts for FilenameAndCounts in lstFilenamesAndCounts )
print("")
print(f"{lstFilenamesAndCounts=}")
print("")
print(strFilenamesAndCounts)

# print DASHBOARD info 
# Ex. DASHBOARD_INFO:DUALS_MedAdv_AH_AZ_202407_202409_20250128.085118.txt.gz 26143,18666102,421248 
lstDashboardInfo = [f"DASHBOARD_INFO:{filename.ljust(50)} {counts}" for filename, counts in zip (COPY_INTO_FILENAMES, ROW_INFO) ]
strDashboardInfo = "\n".join(sDashboardInfo for sDashboardInfo in lstDashboardInfo)  + "\n"
print("")
print(strDashboardInfo)
#  
sys.exit(0)


sFilename = "P#EFT.ON.PSPSQ5.D241031.T0950051"

idx = sFilename.find("PSPSQ")
if idx == -1:
    print("Error")
else:
    sQtr = sFilename[(idx + 4) : (idx + 6) ]

idx = sFilename.find(".D2")
if idx == -1:
    print("Error")
else:
    sRunDtYYYYMMDD = "20" + sFilename[(idx + 2) : (idx + 8) ]
    sRunDtYYYY = sRunDtYYYYMMDD[:4]


print(f"{sQtr=}")
print(f"{sRunDtYYYYMMDD=}")
print(f"{sRunDtYYYY=}")

sys.exit(0)

#lstsFilename.split(".")

        # find node that begins with D2








from os.path import basename 

import platform
 
hostname = platform.node()
print("Hostname:", hostname)

sys.exit(0)


sTest = "ASC_PTB|ASC Part B|A||Apr|LW|N||EFT||||Y\r\nblbtn_clm_ext|Blue Button|W|MON|||N||EFT||||Y\r\nblbtn_drug_prvdr_ext|Blue Button|W|FRI|||N||EFT||||Y\r\nCreditable Coverage|Creditable Coverage - ETL (Heads-Up)|A||AUG|1|Y||SF||||N\r\nDeath Master|Death Master|M|FW|||Y||UNOS web|||Y|N\r\nDemoFinderFileExtracts|DEMO Finder |M|5|||Y|MF|EFT|Y|||N\r\nDRG|DRG|A||JUL|7|||Excel-DDOM||||\r\nDSH|DSH Extract|W|M-F|||Y||Box|N|||N\r\nFMR|FMR - ETL|S||APR,OCT|16|N||SF||||N\r\nFMR|FMR-Extract|S||APR,OCT|16|N||EFT||Y||N\r\nHCPP|HCPP - (MAC Carrier Clm Rpt)  (Heads-Up)|A||SEP|FW|Y|Email|EFT||||N\r\nHOS|HOS - Health Outcome Survey|S||JAN,APR|LW|Y|Excel|Box||||N\r\nHSAF|HSAF (non-IDR) (EDX#200,EDX#210)|A||JUN |FW|||MF|Y|||Y\r\nMEDPAC |MEDPAC - MBD/CME data for HSP Ext|A||JUL|30|N||Box||||N\r\nBAYSTATE|MEDPAR Baystate|S||JAN,APR|29|Y||EFT||||N\r\nBAYSTATE|MEDPAR Baystate (Optional)|S||APR|29|Y||EFT||||N\r\nBAYSTATE_RRB|MEDPAR Baystate|S||JAN,APR|29|Y||EFT||||N\r\nBAYSTATE_RRB|MEDPAR Baystate (Optional)|S||APR|29|Y||EFT||||N\r\nMNUP_MED_NONUTIL_ext|MNUP Annual|A||AUG|25|Y||EFT||||N\r\nMNUP_MED_NONUTIL_Monthly_ext|MNUP Monthly|M|FW|| |Y||EFT||||N\r\nNYSPAP_Bene_Info|NYSPAP Extract|M|1|||Y||Box||||N\r\nOFM_PDE|OFM PDE|A||JUN,OCT|15|Y|Excel|Box||||N\r\nOPMHI_CAR|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_DME|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_HHA|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_HSP|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_INP|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_OPT|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_SNF|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_PDE|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nOPMHI_ENRLMNT|OPMHI (PTA PTB PTD)|Q||JAN,APR,JUL,OCT|15|Y||Box|Y|||N\r\nPartABMonthly |Part A/B Monthly Payments |M|12|||N||SAS email|||Y|Y\r\nPart ABDEnrollment  |Part A/B/D Enrollment Reports (MSTR)|A||MAY|FW|N||Sub||||Y\r\nDEA_PECOS|PECOS|M|FW|||N||EFT||||Y\r\nPBAR-MSTR|PBAR MSTR Subscription Rpts|A||AUG|1|N||Email||||Y\r\nPSPS|PSPS Extract Q1 Q5|Q||Apr|25|N||EFT||||Y\r\nPSPS|PSPS Extract Q2 Q6|Q||Jul|25|N||EFT||||Y\r\nPSPS|PSPS Extract Q3|Q||Oct|25|N||EFT||||Y\r\nPSPS|PSPS Extract Q4|Q||Jan|25|N||EFT||||Y\r\nPSPS_Split_files|PSPS HCPS Split Q6|Q||Jul|25|N||EFT||||Y\r\nPSPS_Supress|PSPS Suppress Q6|Q||Jul|25|N||EFT|||Y|Y\r\nPSPS_NPI|PSPS_NPI_EXTRACT|S||Jan,Jul|20|N||EFT|||Y|Y\r\nPartB_Carrier|Part B Carrier - Early|Q||Apr|1|N||EFT||||Y\r\nPartB_Carrier|Part B Carrier - Final|Q||Jul|1|N||EFT||||Y\r\nPartB_Carrier|Part B Carrier - M12|Q||Jan|1|N||EFT||||Y\r\nPTD_Duals|Part D Duals Daily|W|M-F|||N||EFT||||Y\r\nPTD_Duals|Part D Duals Monthly |M|LW|||N||EFT||||Y\r\nPHYZIP_SUM|PHYZIP Sum|A|  |JUL|FRI-2|N||EFT||||Y\r\nRAC|RAC - Mainframe|M|12|||N||EFT|Y|||Y\r\nRAC|RAC - Back-up GDG before NOV 2025 run|A||OCT|12|N||EFT|Y|||Y\r\nRAC|RAC - Ask James Gao to change EFT Dest|S||SEP,OCT|12|N||EFT|Y|||Y\r\nRAND_FFS_PTA_HHA|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_FFS_PTA_HOS|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_FFS_PTA_CAR|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_FFS_PTA_DME|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_FFS_PTA_INP|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_FFS_PTA_OPT|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_FFS_PTA_SNF|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nRAND_PTD|RAND FFS - A, B, D|A||JAN|15|N||Box|N|N|N|N\r\nSAF_ PDE|SAF PDE |A||SEP|FW|N||S3 |N|N|N|N\r\nSAFENC_ CAR|SAFENC - CAR  (Final)|S||OCT|24|N||EFT|Y||Y|N\r\nSAFENC_CAR|SAFENC - CAR  (Early)|S||MAR|9|N||EFT|Y||Y|N\r\nSAFENC_DME|SAFENC - DME  (Final)|S||OCT|8|N||EFT|Y||Y|N\r\nSAFENC_DME|SAFENC - DME  (Early)|S||MAR|5|N||EFT|Y||Y|N\r\nSAFENC_HHA|SAFENC - HHA  (Final)|S||SEP|11|N||EFT|Y||Y|N\r\nSAFENC_HHA|SAFENC - HHA  (Early)|S||FEB|7|N||EFT|Y||Y|N\r\nSAF_ENC_INP_SNF|SAFENC - INP  (Final)|S||SEP|29|N||EFT|Y||Y|N\r\nSAF_ENC_INP_SNF|SAFENC - INP  (Early)|S||FEB|26|N||EFT|Y||Y|N\r\nSAFENC_ OPT|SAFENC - OPT  (Final)|S||SEP|25|N||EFT|Y||Y|N\r\nSAFENC_ OPT|SAFENC - OPT  (Early)|S||FEB|12|N||EFT|Y||Y|N\r\nSAF_ENC_INP_SNF|SAFENC - SNF  (Final)|S||OCT|5|N||EFT|Y||Y|N\r\nSAF_ENC_INP_SNF|SAFENC - SNF  (Early)|S||FEB|28|N||EFT|Y||Y|N\r\nSTS_HHA_AA7|STS HHA AA7 - (A4A)|S||JAN,JUL|FRI-2|N||Box|N|||Y\r\nSTS_HHA_RevCtr_Rpts|STS HHA Rev Ctrs Rpt - (AA5)|S||JAN,JUL|FRI-2|N||Box|N|||Y\r\nSTS_HHA_Facility_Rpt|STS HHA Facility Rpt - (AA4)|S||JAN,APR,JUL,OCT|FRI-2|N||Box|N|||Y\r\nSTS_HOS_Facility_Rpt|STS HOS Facility Rpt -  (AA6)|S||JAN,APR,JUL,OCT|FRI-2|N||Box|N|||Y\r\nSTS_MED_INS_Tbl_Rpts|STS Med Ins Rpt - (BB2A)|S||JAN,JUL|FRI-2|N||Box|N|||Y\r\nSTS_MED_INS_MN_Rpts|STS Med Ins MN Rpt - (BB2A)|S||JAN,JUL|FRI-2|N||Box|N|||Y\r\nSTS_PTA_BillsPymts_Rpts|STS PTA Bills Paymts Rpt - (A-1AB)|S||JAN,JUL|FRI-2|N||Box|N|||Y\r\nSTS_PTA_BillsPymts_MN_Rpts|STS PTA Bills Paymts MN Rpt - (A-1AB) |S||JAN,JUL|FRI-2|N||Box|N|||Y\r\nSTS_SNF_RPTS|STS SNF Rpt - (AA8)|Q||JAN,APR,JUL,OCT|FRI-2|N||Box|N|||Y\r\nTRICARE|Tricare|W|WED|||Y|MF|EFT|Y|||N\r\nVAPTD|VA Part D|Q||MAR,JUN,SEP,DEC|FW|Y||VA Box|N|||N\r\nVARTN|VA Return -  (Heads-Up)|A||AUG|LW|Y||VA Box||Y||N\r\nWA  MED ENRLMT MS|Washington St Medicare Enrollment (MS)|A||APR|1|N||SUB|N|N|N|Y\r\n"

fld = None

if fld == None:
    print("its None")
else:
    print("not None")

#lstConfigRecs = sTest.split('\r\n')
lstConfigRecs = sTest.splitlines()
print (len(lstConfigRecs))

for rec in lstConfigRecs:
    print(f"{rec=}")

print("")

newline = os.linesep

sConfigFileInfo = (os.linesep).join([str(ConfigRec) for ConfigRec in lstConfigRecs])
print(sConfigFileInfo.encode('utf-8'))

sys.exit(0)


















SFUI_Files_List = []
FromDt = '2025-04-08'
ToDt = '2025-04-08'

filenamesNPath2Attach='/app/IDRC/XTR/CMS/PartAB_Year_20250611.151951.csv,/app/IDRC/XTR/CMS/PartAB_Month_20250611.151951.csv'

lstAttachments = filenamesNPath2Attach.split(",")
print(f"{len(lstAttachments)=}")

for sAttFilenameNPath in lstAttachments: 
    basefilename = basename(sAttFilenameNPath)
    print(f"{basefilename=}")





def resp_to_filelist(resp):

    print(f"In function resp_to_filelist" )

    # Exclude ETag; Filter out results that are not within date range
    return [{'Key': x['Key'], 'tmstmp': x['LastModified'].strftime('%Y%m%d.%H%M%S'), 'bytes': x['Size'], 'StorClass': x['StorageClass']} for x in resp['Contents'] if  FromDt <= x['LastModified'].strftime('%Y-%m-%d') <= ToDt]


resp = "{'Key': 'xtr/DEV/FOIA/FOIA_SFUI_TOUHY_MICHAEL_CARTER_MA_2023.txt.gz', 'LastModified': datetime.datetime(2025, 4, 8, 20, 17, 6), 'ETag': 'ca1fb22e5c70e3e9c6985e9f1196464e-3', 'ChecksumAlgorithm': ['CRC64NVME'], 'Size': 39156600, 'StorageClass': 'STANDARD'}"

SFUI_Files_List.extend(resp_to_filelist(resp))



sys.exit(0)



resp={'ResponseMetadata': {'RequestId': 'TS07JVB2EVK75H19', 'HostId': 'Cnx2BineTxjDrKU0/iN6ZcjfJUlJz9kg2bZMy/D59X4J2+dPBS9TOXkCsLchA3zTCMCXeDOH1KM=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'Cnx2BineTxjDrKU0/iN6ZcjfJUlJz9kg2bZMy/D59X4J2+dPBS9TOXkCsLchA3zTCMCXeDOH1KM=', 'x-amz-request-id': 'TS07JVB2EVK75H19', 'date': 'Tue, 08 Apr 2025 16:56:09 GMT', 'x-amz-bucket-region': 'us-east-1', 'content-type': 'application/xml', 'transfer-encoding': 'chunked', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'IsTruncated': False, 'Name': 'aws-hhs-cms-eadg-bia-ddom-extracts-nonrpod', 'Prefix': 'xtr/DEV/DOJ/DOJ_TOUHY', 'MaxKeys': 1000, 'EncodingType': 'url', 'KeyCount': 0}

if resp['KeyCount'] == 0:
    print("KeyCount") 

sys.exit(0)


ext_filename = "DOJ_TOUHY_MICHAEL_CARTER_MA_2015.txt.gz"
ext_filename_1st_3_nodes = ""
NOF_Delim = 0

for ch in ext_filename:
    if ch == '_':
        NOF_Delim += 1
        if NOF_Delim == 3:
            break
            
    ext_filename_1st_3_nodes += ch

print(ext_filename_1st_3_nodes)

sys.exit(0)


sJOBDTLS_Recs = """{'log': 'DOJ_TOUHY_MICHAEL_NOLOG_20250221.202249.log', 'ext': 'DOJ_TOUHY_MICHAEL_', 'runTmstmp': '20250221.202249', 'ExtractFile': 'DOJ_TOUHY_MICHAEL_CARTER_MA_2022.txt.gz', 'RecCount': 337141, 'FileByteSize': 779469992, 'HumanFileSize': '743 MB'}
{'log': 'DOJ_TOUHY_MICHAEL_NOLOG_20250221.202249.log', 'ext': 'DOJ_TOUHY_MICHAEL_', 'runTmstmp': '20250221.202249', 'ExtractFile': 'DOJ_TOUHY_MICHAEL_CARTER_MA_2022.txt.gz', 'RecCount': 337141, 'FileByteSize': 779469992, 'HumanFileSize': '743 MB'}
"""
json_obj = json.dumps(sJOBDTLS_Recs)
print(type(json_obj))
print(json_obj)

sys.exit(0)

#args.bucket = 'aws-hhs-cms-eadg-bia-ddom-extracts-nonrpod/xtr/DEV/Dashboard/'
#args.bucket = 'aws-hhs-cms-eadg-bia-ddom-extracts/xtr/Dashboard/'
BktFldrNFilePrefix = "aws-hhs-cms-eadg-bia-ddom-extracts/xtr/DOJ/DOJ_TOUHY"
#DashboardFldr = "aws-hhs-cms-eadg-bia-ddom-extracts-nonrpod/xtr/DEV/Dashboard/"
print("")
print(f"{BktFldrNFilePrefix=}")

BktFldrNFilePrefixParts = BktFldrNFilePrefix.split("/", 1)
BktFldrNFilePrefixPartsLen = len(BktFldrNFilePrefixParts)

# Get the bucket name 
bucketname = BktFldrNFilePrefixParts [0]

# Get the folder path and file prefix 
# Ex. folder_n_file_prefix = 'xtr/DOJ/DOJ_SFUI' or 'xtr/FOIA/FOIA_SFUI' or 'xtr/DOJ/DOJ_TOUHY'
folder_n_file_prefix = BktFldrNFilePrefixParts[1]

print(f"{bucketname=}")
print(f"{folder_n_file_prefix=}")


# Remove file prefix from folder_n_file_prefix 
# Ex. xtr/DEV/DOJ/DOJ_TOUHY --> xtr/DEV/
# Ex. xtr/DOJ/DOJ_TOUHY --> xtr/
FldrNFilePrefixParts = folder_n_file_prefix.split("/")
FldrNFilePrefixPartsLen = len(BktFldrNFilePrefixParts) 

BktXTRFolderLen = BktFldrNFilePrefixPartsLen - 2
print(f"{BktXTRFolderLen=}")
bucketNHLFldr = "/".join(BktFldrNFilePrefixParts [ : BktXTRFolderLen ])
print(f"{bucketNHLFldr=}")

TMSTMP="20250407.121314"
# DASHBOARD_JOB_DTLS_EXTRACT_FILES_20250328.121155.json
global S3DashboardFldr 
S3DashboardFldr = bucketNHLFldr + f"/Dashboard/"
S3DashboardFldr = bucketNHLFldr + f"/Dashboard/"

S3DashboardFldr = bucketNHLFldr + f"DASHBOARD_JOB_DTLS_EXTRACT_FILES_{TMSTMP}.json" 
print(f"{S3DashboardFldr=}")

#DASHBOARD_JOB_DTLS_EXTRACT_FILES_{TMSTMP}.json
#DASHBOARD_JOB_INFO_{TMSTMP}.json

sys.exit(0)


EXT_YR="2023"
EXT_YY=str(EXT_YR)[2:4]

sJOBDTLS_Recs : str = ""

DASHBOARD_JOB_DTLS="{'log': 'DOJ_TOUHY_MICHAEL_NOLOG_20250221.203247.log', 'ext': 'DOJ_TOUHY_MICHAEL_', 'runTmstmp': '20250221.203247', 'ExtractFile': 'DOJ_TOUHY_MICHAEL_CARTER_MA_2024.txt.gz', 'RecCount': 367795, 'FileByteSize': 850342040, 'HumanFileSize': '810 MB'}"
newline= "\n"
sJOBDTLS_Recs += newline
sJOBDTLS_Recs = sJOBDTLS_Recs + str(DASHBOARD_JOB_DTLS) 
sJOBDTLS_Recs += newline
sJOBDTLS_Recs = sJOBDTLS_Recs + str(DASHBOARD_JOB_DTLS) 
sJOBDTLS_Recs += newline
sJOBDTLS_Recs = sJOBDTLS_Recs + str(DASHBOARD_JOB_DTLS) 
sJOBDTLS_Recs += newline

sJOBDTLS_Recs2="""
Record 1
Record 2
Record 3

"""
print(sJOBDTLS_Recs2)

sys.exit(0)


s = b'GeeksForGeeks@12345678' 
s = gzip.compress(s) 
  
# using gzip.decompress(s) method 
unzipped_content = gzip.decompress(s) 
print(type(unzipped_content))
print(unzipped_content) 

print(sys.getsizeof(s))
print(sys.getsizeof(unzipped_content))

cnt = unzipped_content.count(b'\n')
print(f"{cnt=}")

sys.exit(0)

unzipped_stream : str = """Record 5
Record 1
Record 2
Record 3
Record 4
"""

print(unzipped_stream.count('\n'))

sys.exit(0)
ext_filename = "DOJ_TOUHY_MICHAEL_CARTER_MA_2024.txt.gz"

ext_filename_1st_3_nodes = ""
NOF_Delim = 0

for ch in ext_filename:
    ext_filename_1st_3_nodes += ch
    if ch == '_':
        NOF_Delim += 1
        if NOF_Delim == 3:
            break

print(f"{ext_filename_1st_3_nodes=}")        