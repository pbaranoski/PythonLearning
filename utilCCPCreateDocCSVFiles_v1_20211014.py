# utilCCPCreateDocCSVFiles.py
# Paul Baranoski - 10/4/2021

import os
import sys
#from numpy import exp
import pandas
import re

in_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCP documentation\InFiles"
out_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCP documentation\OutFiles"

class InvalidTableDFException(Exception):
    "Tables Data Frame has incorrect number of columns."
class InvalidColsDFException(Exception):
    "Columns Data Frame has incorrect number of columns."

################################
# functions
################################
def processSQLFile(in_file, out_file):

    #print("Start function processSQLFile")

    try: 

        bCommentStrt = False
        bCommentEnd = False
        bInComment = False
        bInIDRCommand = False
        bIDRCall = False
        bSelectStmt = False
        bInsertStmt = False

        arrSelectStmt = []

        # process file
        with open(in_file,"r") as iftxt:

            # truncate output file if exists
            if os.path.exists(out_file):
                os.truncate(out_file, 0)

            # read entire input file
            inrecs = iftxt.readlines()

            for inrec in inrecs:
                # remove leading and trailing spaces
                rec = inrec.strip()

                #skip blank lines
                if rec == "":
                    continue

                ################################
                # Set boolean values
                ################################
                if rec.find('/*') >= 0:
                    bCommentStrt = True
                else:
                    bCommentStrt = False

                if rec.find('*/') >= 0:
                    bCommentEnd = True
                else:
                    bCommentEnd = False

                if rec.find(';') >= 0:
                    bSemiColon = True
                else:
                    bSemiColon = False

                ################################
                # Process multi-line comments
                ################################
                if bCommentStrt:
                    if bCommentEnd:
                        bInComment = False
                    else:
                        bInComment = True    
                    continue
                elif bInComment:
                    if bCommentEnd:
                        bInComment = False
                    continue

                ################################
                # Process single line comments
                ################################
                if rec[0:2] == '--':
                    continue

                ################################
                # Process IDR commands
                ################################
                if rec[0:1] == '.':
                    if bSemiColon:
                        pass
                    else:
                        bInIDRCommand = True
                    continue    
                elif bInIDRCommand:  
                    if bSemiColon:
                        bInIDRCommand = False
                    continue    

                ################################
                # Process IDR SQL commands
                ################################
                if rec[0:5].upper() == 'CALL ' or rec[0:8].upper() == 'COLLECT ' :
                    if bSemiColon:
                        pass
                    else:
                        bIDRCall = True
                    continue    
                elif bIDRCall:  
                    if bSemiColon:
                        bIDRCall = False
                    continue    

                ################################
                # Skip Create/Drop Table line   
                ################################
                if ((rec.upper().find("DROP TABLE") >= 0) or
                    (rec.upper().find("CREATE TABLE") >= 0) or
                    (rec.upper().find("CREATE MULTISET TABLE") >= 0) 
                    ):
                    continue

                ################################
                # Parse for SELECT statement
                ################################
                if  rec[0:6].find("SELECT") >= 0:
                    bSelectStmt = True
                    arrSelectStmt.append(rec)
                    continue
                elif bSelectStmt:
                    arrSelectStmt.append(rec) 
                    if bSemiColon:
                        bSelectStmt = False
                        # parse SELECT Statement
                        processSelectStmt(arrSelectStmt)
                        arrSelectStmt.clear()
                        continue

                    continue

                ################################
                # Parse for INSERT statement
                # --> Can add logic to process INSERT statements
                ################################
                if  rec[0:6].find("INSERT") >= 0:
                    bInsertStmt = True
                    continue
                elif bInsertStmt:
                    continue        

            ################################
            # End of parsing records in file
            ################################    
            else:
                #print("END OF FILE")
                if bSelectStmt:
                    processSelectStmt(arrSelectStmt)

    except Exception as ex:
        print("Exception occurred in function processSQLFile. ")
        print(ex.with_traceback)


def processSelectStmt(arrSelectStmt):

    #print("Start function ProcessSelectStmt ")

    arrTableLines = []
    arrColumns = []
    sFROMJOINStmt = ""
    bFROMJOINCont = False

    try:

        for rec in arrSelectStmt:

            ################################
            # Extract table names
            ################################
            rec = rec.replace("&DBENV.","PRD")
            rec = rec.replace("$ENVNAME","PRD")
            rec = rec.upper()

            #print(rec)    

            ##############################################################
            # Extract Table names 
            # FROM/JOIN and table can span 2 lines
            # Beware the below SQL -->
            # Ex.    THEN  ADD_MONTHS(( BENE_FCT_OBSLT_DT - EXTRACT(DAY
            #               FROM BENE_FCT_OBSLT_DT) + 1),1)-1
            ##############################################################
            if  rec[0:4].find("FROM") >= 0 or rec.find("JOIN") >= 0:
                if rec.find(".") >= 0:
                    arrTableLines.append(rec)
                else:    
                    bFROMJOINCont = True
                    sFROMJOINStmt = rec
                continue
            elif bFROMJOINCont:
                bFROMJOINCont = False
                if rec.find(".") >= 0:
                    arrTableLines.append(sFROMJOINStmt+ " "+rec) 

                sFROMJOINStmt = ""
                continue

            #################################################
            # Create separation between items to create tokens
            # to find columns.
            #################################################                
            rec = rec.replace("="," ")
            # substr(col,1,5) --> col15
            rec = rec.replace(","," ")
            rec = rec.replace("("," ")
            rec = rec.replace(")"," ")

            #################################################
            # Skip columns in ORDER BY phrase
            #################################################                
            #if rec.find("ORDER BY") >= 0:
            #    bOrderByPhrase = True
            #if bOrderByPhrase:
            #    continue

            #################################################
            # remove embedded spaces in a line with a column
            # Ex: "CLEOPP. CLM_LINE_OTHR_PYR_PMT_SQNC_NUM"
            #################################################
            if rec.find(". ") >= 0:
                # remove embedded space between symbolic and column name
                rec = rec.replace(". ", ".")

            #################################################
            # Break line into tokens to find column names
            #################################################
            tokens = rec.split(" ")

            for token in tokens:
                # Token contains possible column name    
                if token.find(".") >= 0:
                    cleanToken = token.replace("'","")

                    # skip format numeric fields  --> .9999"
                    if cleanToken.find(".9") >= 0:
                        continue

                    # FORMAT 'yyyymmddBHH:MI:SS.S(6)'
                    if cleanToken.find("HH:MI:SS.S") >= 0:
                        continue

                    #print(cleanToken)
                    arrColumns.append(cleanToken)
                ##\/**pgb    
                # potential column; do not include renaming COLUMN     
                elif token.find("_") >= 0:
                    if token.find("CURRENT_DATE") >= 0:
                        continue
                    elif token.find("ADD_MONTHS") >= 0:
                        continue
                    elif token.find("TO_DATE") >= 0:
                        continue
                    elif token.find("CHAR_LENGTH") >= 0:
                        continue                    
                    elif rec.upper().find("AS ") == -1:
                        sUnknownSymbolic = "?."  
                        arrColumns.append(sUnknownSymbolic+token)  
                        #print("Taylor --> "+ token)  
                        #print(rec)  
                ##/\**PGB    

        ######################################
        # End of parsing SELECT statement
        ######################################
        print("End of parsing Select statement\n")

        ######################################
        # Create output records
        ######################################
        MergeTblAndCols(arrTableLines, arrColumns)

    
    except Exception as ex:
        print("Exception in function ProcessSelectStmt")
        print(ex.with_traceback)


def MergeTblAndCols(arrTableLines, arrColumns):

    print("Start function MergeTblAndCols ")

    try:

        ######################################
        # Extract table names from text
        ######################################
        #print(arrTableLines)
        idrTables = []

        for tbl in arrTableLines:
            tbl = tbl.replace("FROM ","")
            tbl = tbl.replace("JOIN","")
            tbl = tbl.replace("INNER","")
            tbl = tbl.replace("OUTER","")
            tbl = tbl.replace("LEFT ","")
            tbl = tbl.replace("RIGHT ","")
            tbl = tbl.replace("ON","")
            tbl = tbl.replace(" AS "," ")
            tbl = str(tbl.strip())

            # make all the delimiters the same (space)
            # Ex. schema.table symbol
            tbl = tbl.replace("."," ")

            ##################################################################
            # Replace multiple imbedded spaces with single space
            # I want schema, table, symbol --> extra space adds extra column
            # when string is split by space
            # Ex. schema table  symbol (2 spaces between table and symbol)
            ##################################################################
            tbl = re.sub('\\s+', ' ', tbl)
            #print(tbl)

            tblTokens = tbl.split(" ")
            idrTables.append(tblTokens)
            #print (tblTokens)


        ####################################
        # Build DataFrame of IDR Tables
        ####################################
        #print("Create Tables Data Frame")
        dfIDRTables = pandas.DataFrame(idrTables)

        # Verify that Data Frame has correct # of columns
        NOFTblCols = len(dfIDRTables.columns)
        if NOFTblCols == 3:
            print("Tables Data Frame has correct # of columns! ")  
        else:      
            print(dfIDRTables)
            raise InvalidTableDFException(NOFTblCols)

        # Add column headers to Data Frame
        dfIDRTables.columns = ['Schema','Table','Symbol']
        #dfIDRTables.to_csv(out_file, sep=',')


        ######################################
        # Build DataFrame of IDR Column Names
        ######################################
        #print("Create Columns Data Frame")

        # remove duplicates
        uniqColumns = set(arrColumns)
        #print("NOF columns: "+str(len(uniqColumns)))

        # create list from each column entry: symbolic, column_name
        idrCols = []
        for col in uniqColumns:
            colTokens = col.split(".")
            idrCols.append(colTokens)

        # Create Data Frame
        dfIDRCols = pandas.DataFrame(idrCols)
        
        # Verify that Data Frame has correct # of columns
        NOFTblCols = len(dfIDRCols.columns)
        if NOFTblCols == 2:
            print("Columns Data Frame has correct # of columns! ")  
        else:      
            print(dfIDRCols)
            raise InvalidColsDFException(NOFTblCols)

        # Add column headers to Data Frame
        dfIDRCols.columns = ['Symbol', 'ColName']
        #dfIDRCols.to_csv(out_file, sep=',')

        ####################################################
        # Merge Data Frames --> join columns to table names
        #####################################################
        # left join Data Frames
        dfJoin = dfIDRCols.merge(dfIDRTables, left_on="Symbol", right_on="Symbol", how="left")
        # inner join Data Frames
        #dfJoin = dfIDRCols.merge(dfIDRTables, left_on="Symbol", right_on="Symbol", how="inner")
    
        # 0 represents row-wise sorting and 1 represents column-wise sorting.
        dfSort = dfJoin.sort_values(by=['Schema', 'Table','ColName'], axis=0, ascending=True, kind='mergesort')


        ########################################################
        # Write (append) to csv file w/o header or index column
        ########################################################
        bFileExists = os.path.exists(out_file)
        dfSort.to_csv(out_file, mode='a' if bFileExists else 'w', sep=',', index=False, header=False, columns=["Schema","Table", "ColName", "Symbol"])

    except InvalidTableDFException as ex1: 
        print(f"Exception in MergeTblAndCols: Table DF has {ex1} columns instead of 3.")

    except InvalidColsDFException as ex1: 
        print(f"Exception in MergeTblAndCols: Columns DF has {ex1} columns instead of 2.")

    except Exception as ex:
        print("Exception in MergeTblAndCols")
        print(ex.with_traceback)
        

##################
# Main
# 1) iterate over Input directory's project sub-directories (i.e., BLUE_BUTTON).
# 2) for each project sub-directory, process each .txt file and write .csv file to Output/project directory
##################
projDirBaseList = (projDirBase for projDirBase in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir,projDirBase)) )

for projDirBase in projDirBaseList:
    #print (projDirBase)
    projDirPath = os.path.join(in_dir,projDirBase)
    #print(projDirPath)
    fileSQLList = (inSQLFile for inSQLFile in os.listdir(projDirPath) if os.path.isfile(os.path.join(projDirPath,inSQLFile)) )
 
    for inSQLFile in fileSQLList:
        #print(inSQLFile)
        in_file = os.path.join(projDirPath,inSQLFile)
        outSQLFile = inSQLFile.replace(".txt",".csv")
        out_file = os.path.join(os.path.join(out_dir,projDirBase), outSQLFile)

        print('*' * 10)
        print(in_file)
        print(out_file)
        processSQLFile(in_file, out_file)

print("Pandas versin: "+pandas.__version__)    



            




      
