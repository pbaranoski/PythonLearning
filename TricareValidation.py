import pandas as pd
import numpy 
import sys
import csv
import os
#import datetime

#cme_csv = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\CME_Tricare_Bogus.csv"
cme_csv = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\CME_MF_EXTRACT_D220202.csv"
idr_csv = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\IDR_Tricare.csv"
#idr_csv = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\IDR_Tricare_D211129.csv"
fSummDiffs = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\SummDiffs.txt"
fDtlDiffs = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\DtlDiffs.csv"

fMACntrctDiffs = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\MACntrctDiffs.txt"
fNameDiffs = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\Tricare conversion to IDR\Data\NameDiffs.txt"


iCtrLastNameDiffs = 0
iCtrMiddleNameDiffs = 0
iCtrFirstNameDiffs = 0
iCtrDeathDateDiffs = 0
iCtrBeneInfoDiffs = 0
iCtrPartADiffs = 0
iCtrPartBDiffs = 0
iCtrMACntrctDiffs = 0
iCtrReasonCodeDiffs = 0

iCtrNOFMatchedRecs = 0

sHdr = "SSN-HICN, BENE_CNTRCT_NUM, BENE_PBP_NUM, CVRG_TYPE_CD, BENE_ENRLMT_BGN_DT, BENE_ENRLMT_END_DT, BENE_ENRLMT_CNTRCT_EFCTV_DT"
arrMACntrctDiffRecs = []
arrNameDiffRecs = []

def buildNameDiffRec(row):

    arrIDRFlds = []
    arrCMEFlds = []

    #########################################################
    # Build string of IDR values
    #########################################################   
    arrIDRFlds.append(row.BENE_LAST_NAME_x[:20])
    arrIDRFlds.append(row.BENE_MIDL_NAME_x[:2])
    arrIDRFlds.append(row.BENE_1ST_NAME_x[:20])
 
    sIDRFlds = ", ".join(arrIDRFlds)

    #########################################################
    # Build string of IDR values
    #########################################################   
    arrCMEFlds.append(row.BENE_LAST_NAME_y[:20])
    arrCMEFlds.append(row.BENE_MIDL_NAME_y[:2])
    arrCMEFlds.append(row.BENE_1ST_NAME_y[:20])
 
    sCMEFlds = ", ".join(arrCMEFlds)

    #########################################################
    # Build array of MA Contract rec differences
    #########################################################  
    arrNameDiffRecs.append(f"{row.idrKey} IDR: {sIDRFlds} --> CME: {sCMEFlds}")


def buildMACntrDiffRec(row):
    
    arrIDRFlds = []
    arrCMEFlds = []

    #########################################################
    # Build string of IDR values
    #########################################################   
    arrIDRFlds.append(row.BENE_CNTRCT_NUM_x)
    arrIDRFlds.append(row.BENE_PBP_NUM_x)
    arrIDRFlds.append(row.CVRG_TYPE_CD_x)
    arrIDRFlds.append(row.BENE_ENRLMT_BGN_DT_x)
    arrIDRFlds.append(row.BENE_ENRLMT_END_DT_x)
    arrIDRFlds.append(row.BENE_ENRLMT_CNTRCT_EFCTV_DT_x)

    sIDRFlds = ", ".join(arrIDRFlds)

    #########################################################
    # Build string of CME values
    #########################################################   
    arrCMEFlds.append(row.BENE_CNTRCT_NUM_y)
    arrCMEFlds.append(row.BENE_PBP_NUM_y)
    arrCMEFlds.append(row.CVRG_TYPE_CD_y)
    arrCMEFlds.append(row.BENE_ENRLMT_BGN_DT_y)
    arrCMEFlds.append(row.BENE_ENRLMT_END_DT_y)
    arrCMEFlds.append(row.BENE_ENRLMT_CNTRCT_EFCTV_DT_y)

    sCMEFlds = ", ".join(arrCMEFlds)

    #########################################################
    # Build array of MA Contract rec differences
    #########################################################  
    arrMACntrctDiffRecs.append(f"{row.idrKey} IDR: {sIDRFlds} --> CME: {sCMEFlds}")


if __name__ == "__main__":

    #########################################################
    # Define variables
    #########################################################
    # create empty data frame with appropriate column names
    dfErrMsgs = pd.DataFrame(columns=["SSN-HICN","ErrMsg"])

    # truncate output file if exists
    if os.path.exists(fSummDiffs):
        os.truncate(fSummDiffs, 0)

    # truncate output file if exists
    if os.path.exists(fDtlDiffs):
        os.truncate(fDtlDiffs, 0)

    # truncate output file if exists
    if os.path.exists(fMACntrctDiffs):
        os.truncate(fMACntrctDiffs, 0)

   # truncate output file if exists
    if os.path.exists(fNameDiffs):
        os.truncate(fNameDiffs, 0)

    #########################################################
    # Read CME and IDR csv files into Pandas Data Frames
    #########################################################
    dfCME = pd.read_csv(cme_csv, dtype=str, na_filter=False,  
        converters={ 'BENE_PTB_NENTLMT_RSN_CD' : lambda x : str(x).strip() } )
    dfIDR = pd.read_csv(idr_csv, dtype=str, na_filter=False,  
        converters={'BENE_PTB_NENTLMT_RSN_CD' : lambda x : str(x).strip() })
 
    dfCME["cmeKey"] = dfCME["BENE_SSN_NUM"] + dfCME["BENE_CAN_NUM"] + dfCME["BENE_BIC_CD"]
    dfIDR["idrKey"] = dfIDR["BENE_SSN_NUM"] + dfIDR["BENE_CAN_NUM"] + dfIDR["BENE_BIC_CD"]

    #print(dfIDR)
    #########################################################
    # write summary record
    #########################################################
    with open(fSummDiffs,"a") as fobj:
        nofRecs = len(dfCME)
        fobj.write(f"            NOF CME record(s): {nofRecs}\n")

        nofRecs = len(dfIDR)
        fobj.write(f"            NOF IDR record(s): {nofRecs}\n")
 
    #########################################################
    # Join CME and IDR Data Frames by Key: (SSN/HICN)
    #########################################################
    dfDiffs = dfIDR.merge(dfCME, left_on="idrKey", right_on="cmeKey", how="outer")
    print("dfDiffs:")
    print (dfDiffs)

    #########################################################
    # Find rows where CME key is missing 
    # --> write to detail error file
    #########################################################
    dfMissing = dfDiffs.loc[dfDiffs["cmeKey"].isnull()]
    nofRecs = len(dfMissing)

    if nofRecs > 0:
        # create new DF with Key columns; add errMsg col; drop null column; rename columns
        dfMissing = dfMissing[["cmeKey","idrKey"]]
        dfMissing["ErrMsg"] = "No matching CME Key found" 
        dfMissing.drop(["cmeKey"], axis="columns", inplace=True)
        dfMissing.rename(columns = {'idrKey':'SSN-HICN'}, inplace = True)
        
        print("dfMissing:")
        print(dfMissing)

        # Add new error msgs to on-going Error msgs
        dfErrMsgs = dfErrMsgs.append(dfMissing, ignore_index=True)

        print("dfErrMsgs:")
        print(dfErrMsgs)

        # drop unmatched records from diffs Data Frame
        dfDiffs.dropna(axis=0, subset=['cmeKey'], inplace=True)
    
    #########################################################
    # write summary record
    #########################################################
    with open(fSummDiffs,"a") as fobj:
        fobj.write(f"  None Matching CME record(s): {nofRecs}\n")

    #########################################################
    # Find rows where IDR record is missing 
    # --> write to detail error file
    #########################################################
    dfMissing = dfDiffs.loc[dfDiffs["idrKey"].isnull()]
    nofRecs = len(dfMissing)

    if nofRecs > 0:
        # create new DF with Key columns; add errMsg col; drop null column; rename columns
        dfMissing = dfMissing[["cmeKey","idrKey"]]
        dfMissing["ErrMsg"] = "No matching IDR Key found" 
        dfMissing.drop(["idrKey"], axis="columns", inplace=True)
        dfMissing.rename(columns = {'cmeKey':'SSN-HICN'}, inplace = True)
        
        print("dfMissing:")
        print(dfMissing)

        # Add new error msgs to on-going Error msgs
        dfErrMsgs = dfErrMsgs.append(dfMissing, ignore_index=True)

        print("dfErrMsgs:")
        print(dfErrMsgs)

        # drop unmatched records
        dfDiffs.dropna(axis=0, subset=['idrKey'], inplace=True)

    #########################################################
    # write summary record
    #########################################################
    with open(fSummDiffs,"a") as fobj:
        fobj.write(f"  None Matching IDR record(s): {nofRecs}\n")

    #########################################################
    # write summary record
    #########################################################
    nofRecs = len(dfDiffs)
    with open(fSummDiffs,"a") as fobj:
        fobj.write(f"       Paired record(s) found: {nofRecs}\n")

    ##########################################################
    # Identify individual row differences
    ##########################################################
    print("\n\n")

    for row in dfDiffs.itertuples():

        arrDifferences = []
        bNameDiff = False

        #----------------------------------
        # Identify Last Name difference
        #----------------------------------
        if row.BENE_LAST_NAME_x != row.BENE_LAST_NAME_y:
            arrDifferences.append("BENE_LAST_NAME")
            iCtrLastNameDiffs += 1
            bNameDiff = True

        #----------------------------------
        # Identify Death Date difference
        #----------------------------------
        if row.BENE_DEATH_DT_x != row.BENE_DEATH_DT_y:
            arrDifferences.append("BENE_DEATH_DT")
            iCtrDeathDateDiffs += 1

        #----------------------------------
        # Identify MIDDLE Name difference
        # --> Related to LNAME diff
        #----------------------------------
        if row.BENE_MIDL_NAME_x != row.BENE_MIDL_NAME_y:
            arrDifferences.append("BENE_MIDL_NAME")
            iCtrMiddleNameDiffs += 1
            bNameDiff = True

        #----------------------------------
        # Identify FIRST Name differences
        #----------------------------------
        if row.BENE_1ST_NAME_x != row.BENE_1ST_NAME_y:
            arrDifferences.append("BENE_1ST_NAME")
            iCtrFirstNameDiffs += 1
            bNameDiff = True

        if bNameDiff:
            buildNameDiffRec(row)

        #----------------------------------
        # Identify BENE info differences
        #----------------------------------
        iCtrCategoryDiffs = 0

        if row.BENE_BRTH_DT_x != row.BENE_BRTH_DT_y:
            arrDifferences.append("BENE_BRTH_DT")
            iCtrCategoryDiffs += 1

        if row.BENE_SEX_CD_x != row.BENE_SEX_CD_y:
            arrDifferences.append("BENE_SEX_CD")
            iCtrCategoryDiffs += 1

        if row.BENE_PTB_NENTLMT_RSN_CD_x != row.BENE_PTB_NENTLMT_RSN_CD_y:
            arrDifferences.append("BENE_PTB_NENTLMT_RSN_CD")
            iCtrCategoryDiffs += 1

        if row.BENE_MBI_ID_x != row.BENE_MBI_ID_y:
            arrDifferences.append("BENE_MBI_ID")
            iCtrCategoryDiffs += 1

        if iCtrCategoryDiffs > 0:
            iCtrBeneInfoDiffs += 1

        #----------------------------------
        # Identify Part A differences
        #----------------------------------
        iCtrCategoryDiffs = 0

        if row.PTA_ENTLMT_STRT_DT_x != row.PTA_ENTLMT_STRT_DT_y:
            arrDifferences.append("PTA_ENTLMT_STRT_DT")
            iCtrCategoryDiffs += 1

        if row.PTA_ENTLMT_END_DT_x != row.PTA_ENTLMT_END_DT_y:
            arrDifferences.append("PTA_ENTLMT_END_DT")
            iCtrCategoryDiffs += 1

        if row.PTA_ENTLMT_STUS_CD_x != row.PTA_ENTLMT_STUS_CD_y:
            arrDifferences.append("PTA_ENTLMT_STUS_CD")
            iCtrCategoryDiffs += 1

        if iCtrCategoryDiffs > 0:
            iCtrPartADiffs += 1

        #----------------------------------
        # Identify Part B differences
        #----------------------------------
        iCtrCategoryDiffs = 0

        if row.PTB_ENTLMT_STRT_DT_x != row.PTB_ENTLMT_STRT_DT_y:
            arrDifferences.append("PTB_ENTLMT_STRT_DT")
            iCtrCategoryDiffs += 1

        if row.PTB_ENTLMT_END_DT_x != row.PTB_ENTLMT_END_DT_y:
            arrDifferences.append("PTB_ENTLMT_END_DT")
            iCtrCategoryDiffs += 1

        if row.PTB_ENTLMT_STUS_CD_x != row.PTB_ENTLMT_STUS_CD_y:
            arrDifferences.append("PTB_ENTLMT_STUS_CD")
            iCtrCategoryDiffs += 1

        if iCtrCategoryDiffs > 0:
            iCtrPartBDiffs += 1

        #----------------------------------
        # Identify Reason Code differences
        #----------------------------------
        iCtrCategoryDiffs = 0

        if row.RSN_LAST_CHG_DT_x != row.RSN_LAST_CHG_DT_y:
            arrDifferences.append("RSN_LAST_CHG_DT")
            iCtrCategoryDiffs += 1

        if row.BENE_MDCR_ENTLMT_RSN_CD_x != row.BENE_MDCR_ENTLMT_RSN_CD_y:
            arrDifferences.append("BENE_MDCR_ENTLMT_RSN_CD")
            iCtrCategoryDiffs += 1

        if iCtrCategoryDiffs > 0:
            iCtrReasonCodeDiffs += 1

        #----------------------------------
        # Identify MA Contract differences
        #----------------------------------
        iCtrCategoryDiffs = 0

        if row.BENE_CNTRCT_NUM_x != row.BENE_CNTRCT_NUM_y:
            arrDifferences.append("BENE_CNTRCT_NUM")
            iCtrCategoryDiffs += 1

        if row.BENE_PBP_NUM_x != row.BENE_PBP_NUM_y:
            arrDifferences.append("BENE_PBP_NUM")
            iCtrCategoryDiffs += 1 

        if row.CVRG_TYPE_CD_x != row.CVRG_TYPE_CD_y:
            arrDifferences.append("CVRG_TYPE_CD")
            iCtrCategoryDiffs += 1

        if row.BENE_ENRLMT_BGN_DT_x != row.BENE_ENRLMT_BGN_DT_y:
            arrDifferences.append("BENE_ENRLMT_BGN_DT")
            iCtrCategoryDiffs += 1

        if row.BENE_ENRLMT_END_DT_x != row.BENE_ENRLMT_END_DT_y:
            arrDifferences.append("BENE_ENRLMT_END_DT")
            iCtrCategoryDiffs += 1

        if row.BENE_ENRLMT_CNTRCT_EFCTV_DT_x != row.BENE_ENRLMT_CNTRCT_EFCTV_DT_y:
            arrDifferences.append("BENE_ENRLMT_CNTRCT_EFCTV_DT")
            iCtrCategoryDiffs += 1

        if iCtrCategoryDiffs > 0:
            iCtrMACntrctDiffs += 1
            buildMACntrDiffRec(row)

        #----------------------------------
        # write detil error msg  
        #----------------------------------
        if len(arrDifferences) > 0:  
            sDifferences = ', '.join(arrDifferences)
            sDifferences = "Differences: " + sDifferences

            dict_row = {"SSN-HICN":str(row.idrKey),"ErrMsg":sDifferences}
            dfErrMsgs = dfErrMsgs.append(dict_row, ignore_index=True)
        else:
            iCtrNOFMatchedRecs += 1

    ##########################################################
    # Write Summary record
    ##########################################################
    with open(fSummDiffs,"a") as fobj:
        fobj.write(f"  NOF Matched record(s) found: {iCtrNOFMatchedRecs}\n")

    ##########################################################
    # Write out all detail error messages
    ##########################################################
    dfErrMsgs.to_csv(fDtlDiffs,sep = ",", index=False, line_terminator = "\n")

    ##########################################################
    # Write Summary records
    ##########################################################
    with open(fSummDiffs,"a") as fobj:
        fobj.write(f"  Last Name differences found: {iCtrLastNameDiffs}\n")
        fobj.write(f"Middle Name differences found: {iCtrMiddleNameDiffs}\n")
        fobj.write(f" First Name differences found: {iCtrFirstNameDiffs}\n")
        fobj.write(f" Death Date differences found: {iCtrDeathDateDiffs}\n")
        fobj.write(f"  Bene Info differences found: {iCtrBeneInfoDiffs}\n")
        fobj.write(f"     Part A differences found: {iCtrPartADiffs}\n")
        fobj.write(f"     Part B differences found: {iCtrPartBDiffs}\n")
        fobj.write(f"MA Contract differences found: {iCtrMACntrctDiffs}\n")
        fobj.write(f"Reason Code differences found: {iCtrReasonCodeDiffs}\n")

    ##########################################################
    # Write Differences Files
    ##########################################################
    with open(fMACntrctDiffs,"a") as fobj:
        fobj.write(sHdr+"\n")
        for rec in arrMACntrctDiffRecs:
            fobj.write(rec + "\n")

    with open(fNameDiffs,"a") as fobj:
        fobj.write("BENE_LAST_NAME, BENE_MIDL_NAME, BENE_1st_NAME \n")
        for rec in arrNameDiffRecs:
            fobj.write(rec + "\n")

