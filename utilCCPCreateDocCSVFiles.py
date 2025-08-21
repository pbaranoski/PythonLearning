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
                # remove leading and trailing spaces and upper case text
                rec = inrec.strip().upper()
                rec = rec.replace("\t"," ")

                #skip blank lines
                if rec == "":
                    continue

                ################################
                # Set boolean values
                ################################
                if rec [0:2] == '/*':    
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
                # Skip multi-line comments
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
                # Skip single line comments
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
                if rec[0:5] == 'CALL ' or rec[0:8] == 'COLLECT ' :
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
                if ((rec.find("DROP TABLE") >= 0) or
                    (rec.find("CREATE TABLE") >= 0) or
                    (rec.find("CREATE MULTISET TABLE") >= 0) 
                    ):
                    continue

                ##########################################
                # remove in-line comments following 
                #  valid SQL text
                ##########################################
                idx = rec.find("--")
                if idx >= 0:
                    rec = rec[:idx]

                ##########################################
                # remove in-line comments following 
                #  valid SQL text 
                ##########################################
                idxStartComment = rec.find("/*",1) 

                if idxStartComment >= 0:
                    idxEndComment = rec.find("*/") 
                    # remove instream comment
                    codeBeforeComment = rec[0:idxStartComment]
                    codeAfterComment = rec[idxEndComment + 2: ]
                    rec = codeBeforeComment + " " + codeAfterComment
                    # if line is now blank, skip blank line
                    if rec.strip() == "":
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
                        # process SELECT Statement
                        sSelect = cleanseSQLStatment(arrSelectStmt)
                        processSelectStmt(sSelect)
                        arrSelectStmt.clear()
                        continue
                    else:        
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
                    sSelect = cleanseSQLStatment(arrSelectStmt)
                    processSelectStmt(sSelect)


    except Exception as ex:
        print("Exception occurred in function processSQLFile. ")
        print(ex.with_traceback)
        ex.d

def cleanseSQLStatment(arrSelectStmt):

        #########################################
        # Convert SELECT array into single String
        #########################################
        sSelect = ' '.join(arrSelectStmt)
        #print(sSelect)

        # Remove ending semi-colon
        sSelect = sSelect.replace(";","")

        ################################
        # modify parameter placeholders
        ################################
        sSelect = sSelect.replace("&DBENV.","PRD")
        sSelect = sSelect.replace("$ENVNAME","PRD")
        sSelect = sSelect.replace("${ENVNAME}","PRD")

        #################################################
        # Create separation between items to more easily
        # create tokens for processing.
        # (Add space between token if it doesn't exist.)
        #################################################                
        sSelect = sSelect.replace("="," = ")
        sSelect = sSelect.replace(","," , ")
        sSelect = sSelect.replace("'"," ' ")
        sSelect = sSelect.replace("("," ( ")
        sSelect = sSelect.replace(")"," ) ")
        sSelect = sSelect.replace("+"," + ")
        sSelect = sSelect.replace("/"," / ")
        sSelect = sSelect.replace("*"," * ")

        ##############################################################
        # Remove JOIN Qualifier keywords  (to make it easier to parse)
        ##############################################################
        sSelect = sSelect.replace("INNER ","")
        sSelect = sSelect.replace("OUTER ","")
        sSelect = sSelect.replace("LEFT ","")
        sSelect = sSelect.replace("RIGHT ","")
        sSelect = sSelect.replace("CROSS ","")

        ######################################################
        # remove embedded spaces between symbolic and col name
        # Ex: "CLEOPP. CLM_LINE_OTHR_PYR_PMT_SQNC_NUM"
        ######################################################
        sSelect =  sSelect.replace(". ", ".")

        #########################################################
        # replace multiple spaces with single space between text 
        #########################################################
        sSelect = re.sub('\\s+', ' ', sSelect)

        # Remove false "FROM"s from SELECT statement
        sSelect = removeBogusFROMs(sSelect)
        #print(sSelect)

        #########################################################
        # replace multiple spaces with single space between text 
        #########################################################
        sSelect = sSelect.strip()
        sSelect = re.sub('\\s+', ' ', sSelect)

        return sSelect

def processSelectStmt(sSelect):

    #############################################
    # This is a recursive function 
    #   (A function that call itself)
    # Note: sSelect input parameter should not have
    #       beginning or ending parens for this
    #       function to work properly.
    #############################################

    #print("Start function ProcessSelectStmt ")
    arrTables = [] 
    arrColumns = []
    arrSubSelect = []
    arrCurrentSelect = []

    bInitSelect = True

    bSubSelect = False
    bAdditionalSelect = False
    bASActive = False
    bExtractColsFromJoin = False

    eSQLInProcessMode = ""
    eSQLInProcessTokenSeqNum = 0

    sColumnAndSymbol = ""
    iParenCount = 0
    
    try:

        ################################
        # process SELECT statement
        ################################
        tokens = sSelect.split(" ")

        # Ensure that if 1st and last token are parens, that they are initialized to spaces
        if len(tokens) > 0:
            iMaxToken = len(tokens) - 1
            if tokens[0] == "(":
                if tokens[iMaxToken] == ")":
                    tokens[0] = ""
                    tokens[iMaxToken]  = ""
                else:
                    print("Error - mismatched beginning and ending parens")    

        # Main loop processing
        for token in tokens:

            if token == "TAYLOR":
                print(sSelect)
                print("taylor")

            if not bSubSelect:
                arrCurrentSelect.append(token)

            # These IFs should not be part of Main If/Else
            if token == ")":
                iParenCount -= 1

            if token == "(":
                iParenCount += 1

            # process current token
            if bSubSelect:
                if iParenCount == 0:
                    bSubSelect = False
                    
                    print("subSelect")
                    print(arrSubSelect)

                    sSubSelect = ' '.join(arrSubSelect)
                    arrSubSelect = []
                    #print("Call to process subSelect")
                    processSelectStmt(sSubSelect)
                else:  
                    arrSubSelect.append(token)

            elif bAdditionalSelect:
                # Once we see the UNION, MINUS, INTERSECT reserved words
                #     --> collect all other statements and process like a subSelect.
                # The end of the Additional Select is not a Paren, but end-of-tokens
                arrSubSelect.append(token)

            elif token == "SELECT":
                if bInitSelect:
                    bInitSelect = False
                    eSQLInProcessMode = 'S'
                else:
                    bSubSelect = True
                    arrSubSelect.append(token)

                    if (eSQLInProcessMode == "F" or 
                        eSQLInProcessMode == "J"):
                        arrTables.append("?.SUBSELECT_TBL")
                        eSQLInProcessTokenSeqNum = 1

            elif token == "FROM":
                eSQLInProcessMode = 'F'
                eSQLInProcessTokenSeqNum = 0

            elif token == "JOIN":
                eSQLInProcessMode = 'J'
                eSQLInProcessTokenSeqNum = 0
                bExtractColsFromJoin = False

            elif token == "QUALIFY":
                eSQLInProcessMode = 'Q'
                eSQLInProcessTokenSeqNum = 0

            elif token == "UNION":
                eSQLInProcessMode = 'U'
                eSQLInProcessTokenSeqNum = 0
                bAdditionalSelect = True

            elif token == "MINUS":
                eSQLInProcessMode = 'M'
                eSQLInProcessTokenSeqNum = 0                
                bAdditionalSelect = True

            elif token == "INTERSECT":
                eSQLInProcessMode = 'I'
                eSQLInProcessTokenSeqNum = 0                
                bAdditionalSelect = True

            elif token == "WHERE":  
                eSQLInProcessMode = 'W' 
                eSQLInProcessTokenSeqNum = 0

            elif token == "GROUP":  
                eSQLInProcessMode = 'G' 
                eSQLInProcessTokenSeqNum = 0

            #---------------------------------
            # Process SELECT Statement
            #---------------------------------
            elif eSQLInProcessMode == 'S':
                # SELECT statement is active
                if token == "AS":
                    bASActive = True
                    continue
                elif bASActive:
                    # Skip 'AS' Name
                    bASActive = False
                    continue
                else:    
                    sColumnAndSymbol = GetColSymbolAndName(token)
                    if sColumnAndSymbol != "":
                        arrColumns.append(sColumnAndSymbol) 

            #---------------------------------
            # Process QUALIFY Statement
            #---------------------------------
            elif eSQLInProcessMode == 'Q':
                    sColumnAndSymbol = GetColSymbolAndName(token)
                    if sColumnAndSymbol != "":
                        arrColumns.append(sColumnAndSymbol)     

            #---------------------------------
            # Process FROM Statement
            #---------------------------------
            elif eSQLInProcessMode == 'F':
                # FROM statement is active
                eSQLInProcessTokenSeqNum += 1

                # get TableName
                if eSQLInProcessTokenSeqNum == 1:
                    arrTables.append(token)
                elif token == "AS":
                    # SKIP token --> symbol to follow
                    continue    
                else:
                    # get associated symbol for TableName (if exists)
                    item = len(arrTables) - 1
                    arrTables[item] = arrTables[item] + " " + token

            #---------------------------------
            # Process JOIN Statements
            #---------------------------------
            elif eSQLInProcessMode == 'J':
                # JOIN statement is active
                if token == "ON":
                    bExtractColsFromJoin = True

                if bExtractColsFromJoin:                    
                    sColumnAndSymbol = GetColSymbolAndName(token)
                    if sColumnAndSymbol != "":
                        arrColumns.append(sColumnAndSymbol) 

                else:
                    eSQLInProcessTokenSeqNum += 1

                    # get TableName
                    if eSQLInProcessTokenSeqNum == 1:
                        arrTables.append(token)
                    elif token == "AS":
                        # SKIP token --> symbol to follow
                        continue    
                    else:
                        # get associated symbol for TableName (if exists)
                        item = len(arrTables) - 1
                        arrTables[item] = arrTables[item] + " " + token

            #---------------------------------
            # Process WHERE and GROUP BY Stmt 
            #---------------------------------
            elif eSQLInProcessMode == 'W' or eSQLInProcessMode == 'G' :
                # WHERE statement is active
                sColumnAndSymbol = GetColSymbolAndName(token)
                if sColumnAndSymbol != "":
                    arrColumns.append(sColumnAndSymbol) 

            else:
                # bypass token
                pass

        else:
            if bAdditionalSelect:
                bAdditionalSelect = False
                    
                sSubSelect = ' '.join(arrSubSelect)

                print("subSelect")
                print(sSubSelect)

                arrSubSelect = []
                #print("Call to process subSelect")
                processSelectStmt(sSubSelect)       

        ######################################
        # End of parsing SELECT statement
        ######################################
        print("End of parsing Select statement\n")

        ##sTempString = ' '.join(arrCurrentSelect)
        ##print("String that was parsed")
        ##print(sTempString)

        # remove duplicate entries
        arrColumns = list(dict.fromkeys(arrColumns)) 
        print("arrColumns")
        print(arrColumns)

        # remove duplicate entries
        arrTables = list(dict.fromkeys(arrTables)) 

        #############################################
        # If only one table and no Symbol
        #  --> assume all cols are for that table
        # --> add default symbol so Pandas join will 
        #     match table
        #############################################
        if len(arrTables) == 1:
            sTableAndSymbol = arrTables[0]
            # only table name is present --> add symbol
            if len(sTableAndSymbol.split(" ")) == 1:
                arrTables[0] = arrTables[0] + " ?"


        print("arrTables")
        print(arrTables)

        ######################################
        # Create output records
        ######################################
        MergeTblAndCols(arrTables, arrColumns)

    
    except Exception as ex:
        print("Exception in function ProcessSelectStmt")
        print(ex.with_traceback)

def GetColSymbolAndName(token):

    sColSymbolAndName = ""

    # Token contains possible column name    
    if token.find(".") >= 0:

        # skip format numeric fields  --> .9999"
        if token.find(".9") >= 0:
            pass
        elif token.find("HH:MI:SS.S") >= 0:    
            # skip FORMAT 'yyyymmddBHH:MI:SS.S(6)'
            pass
        else:    
            sColSymbolAndName = token

    # potential columns;      
    elif token.find("_") >= 0:
        if token.find("CURRENT_DATE") >= 0:
            pass
        elif token.find("ADD_MONTHS") >= 0:
            pass
        elif token.find("TO_DATE") >= 0:
           pass
        elif token.find("CHAR_LENGTH") >= 0:
            pass                    
        else:
            sUnknownSymbolic = "?."  
            sColSymbolAndName = sUnknownSymbolic+token

    return sColSymbolAndName          

def removeBogusFROMs(sString):

    commands = ["EXTRACT","SUBSTRING"]

    #########################################################
    # Loop thru list of Commands.
    # Search String for all occurrences of command.
    # Remove the " FROM " token from each command occurrence. 
    #########################################################
    for command in commands:

        # Start search at beginning for each command
        idx = 0

        while True:

            idx = sString.find(command,idx)

            # if no occurrences of command --> exit loop
            if idx == -1:
                break

            # Find opening paren of command    
            idxStart = sString.find("(",idx)

            # if paren is not found --> problem
            if idxStart == -1:
                # There is an problem
                break

            # skip past opending paren
            idx = idxStart + 1
            sSearchString = sString[idx :]

            # account for opening paren
            parenCtr = 1

            # search for end-of command    
            for char in sSearchString:
                idx += 1
                if char == "(":
                    parenCtr += 1
                elif char == ")":
                    parenCtr -= 1
                # we have reached end-of command
                if parenCtr == 0:
                    break        


            # remove " FROM " from inside command
            idxEnd = idx
            idx = sString.find(" FROM ",idxStart,idxEnd)
            sString = sString[:idx] + sString[idx+len(" FROM"):] 

    ###############################
    # return value
    ###############################
    return sString


def MergeTblAndCols(arrTableLines, arrColumns):

    print("Start function MergeTblAndCols ")

    try:

        ######################################
        # Extract table names from text
        ######################################
        #print(arrTableLines)
        idrTables = []

        for tbl in arrTableLines:
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
        elif NOFTblCols == 2:
            # add blank symbolic for each table (assuming no symbol found)
            dfIDRTables['Symbol'] = " "
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
projDirBaseList = (dirItem for dirItem in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir,dirItem)) )

for projDirBase in projDirBaseList:
    #print (projDirBase)
    projDirPath = os.path.join(in_dir,projDirBase)
    #print(projDirPath)
    fileSQLList = (inSQLFile for inSQLFile in os.listdir(projDirPath) if os.path.isfile(os.path.join(projDirPath,inSQLFile)) )
 
    for inSQLFile in fileSQLList:
        #print(inSQLFile)
        in_file = os.path.join(projDirPath,inSQLFile)

        # find inSQLFile extension and replace with .csv ext for outSQLFile
        fileAndExt = os.path.splitext(inSQLFile)
        # array has 2 elements: file and ext 
        if len(fileAndExt) == 2:
            outSQLFile = inSQLFile.replace(fileAndExt[1],".csv")
        else:
            outSQLFile = inSQLFile + ".csv"

        out_file = os.path.join(os.path.join(out_dir,projDirBase), outSQLFile)

        print('*' * 10)
        print(in_file)
        print(out_file)
        processSQLFile(in_file, out_file)

print("Pandas versin: "+pandas.__version__)    



            




      
