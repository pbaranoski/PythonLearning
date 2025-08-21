# utilCCPCreateDocCSVFiles.py
# Paul Baranoski - 10/4/2021

import os
from pickle import FALSE
import sys
#from numpy import exp
import pandas
import re

#in_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCP documentation\InFiles"
#out_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCP documentation\OutFiles"


class InvalidTableDFException(Exception):
    "Tables Data Frame has incorrect number of columns."
class InvalidColsDFException(Exception):
    "Columns Data Frame has incorrect number of columns."

################################
# functions
################################
def processSQLFile(in_file, outSQLFile):

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
            if os.path.exists(outSQLFile):
                os.truncate(outSQLFile, 0)

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
            # End of parsing records in file
            ################################    
            else:
                #print("END OF FILE")
                if bSelectStmt:
                    sSelect = cleanseSQLStatment(arrSelectStmt)
                    processSelectStmt(sSelect)
                    #print (f"sSelect: {sSelect}")


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
        #sSelect = sSelect.replace("'"," ' ")
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

    sColInfo = ""
    
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

        ########################
        # Main loop processing
        ########################
        #for token in tokens:
        iterTokens = iter(tokens)

        while(1):
            # Get next token and check for End-of-tokens
            token = next(iterTokens,'EOF')
            if token == "EOF":
                break

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

                if token == "DISTINCT":
                    continue

                if token == "TO_CHAR":
                    sColInfo = extSQLFuncValues(iterTokens, 2)
                    #print (f"scolInfo: {scolInfo}")
                    continue    

                if token == "RPAD":
                    sColInfo = extSQLFuncValues(iterTokens, 2)
                    #print (f"scolInfo: {scolInfo}")
                    continue    

                if token == ",":
                    # parse sColInfo 1) get length of strings
                    #" '%' AS D1", 'C.CLM_HIC_NUM 20 AS CLM_HIC_NUM'
                    StandardizeColInfo(sColInfo)
                    arrColumns.append(sColInfo)
                    sColInfo = ""
                    continue

                sColInfo = ' '.join( (sColInfo, token) )

            #---------------------------------
            # Process QUALIFY Statement
            #---------------------------------
            #elif eSQLInProcessMode == 'Q':
            #        sColumnAndSymbol = GetColSymbolAndName(token)
            #        if sColumnAndSymbol != "":
            #            arrColumns.append(sColumnAndSymbol)     

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


def StandardizeColInfo(sColInfo):
    # parse sColInfo 1) get length of strings
    # " '%' AS D1"  
    # 'C.CLM_HIC_NUM 20 AS CLM_HIC_NUM'
    # "BMER.BENE_SK 'FM000000000000000000' AS BMER_BENE_SK
    # "BMER.BENE_SK 'S00000000000000.0000' AS BMER_BENE_SK
    #  COL   'YYYYMMDD' as DT
    #  
    sColName = ""
    iColLen = 0
    sColStandardInfo = ""

    lstColInfo = sColInfo.strip().split(" ")
    # Column name is present
    if len(lstColInfo) == 4:
        sColName = lstColInfo[0]
        # Is 2nd token a format string?
        sToken = lstColInfo[1] 
        # Token is format string
        #print(sToken)
        if sToken.find("\'") >= 0:
            # Remove quote
            sToken = sToken.replace("\'","")
            sToken = sToken.replace("FM0","0")
            iColLen = len(sToken)
            #print(iColLen)
        else:
            iColLen = lstColInfo[1]    

        sColStandardInfo = f"{sColName} {iColLen} {lstColInfo[2]} {lstColInfo[3]}" 
        print(sColStandardInfo)     


    # first token is not column
    if lstColInfo[0].find(".") == -1:
        sColName = '?.'
        # is it a literal

    else:
        sColName = lstColInfo[0]






def extCASEFuncValues(iterTokens):

    # At this time, only return first column found for CASE statement
    bTHENPhrase = False
    strTHENPhrase = ""
    strToReturn = ""

    funcValues = []

    while(1):
        token = next(iterTokens)

        if token == "WHEN" or token == "END" :
            bTHENPhrase = False

            if strTHENPhrase != "":
                funcValues.append(strTHENPhrase)
                strTHENPhrase = ""

            if token == "END":
                break
            else:  
                continue
           
        if token == "THEN":
            bTHENPhrase = True
            continue

        if token == "ELSE":
            bTHENPhrase = True

            if strTHENPhrase != "":
                funcValues.append(strTHENPhrase)
                strTHENPhrase = ""

        if bTHENPhrase:    
            strTHENPhrase += token


    if len(funcValues) > 0:
        strToReturn = funcValues[0]

    # Clease String
    strToReturn = strToReturn.replace("*","")
    strToReturn = strToReturn.replace("(","")
    strToReturn = strToReturn.replace(")","")    
    strToReturn = strToReturn.replace("-1","")

    return strToReturn 


def extSQLFuncValues(iterTokens, extTokens): 

    # Works for COALESCE and RPAD

    funcValues = []

    while(1):
        token = next(iterTokens)
        if token == "(":
            continue

        if token == "COALESCE":
            token = extSQLFuncValues(iterTokens, 1)
            funcValues.append(token)
            continue

        if token == "CASE":
            token = extCASEFuncValues(iterTokens)
            funcValues.append(token)
            continue            

        if token == ",":
            continue

        if token == ")":
            break
        
        if extTokens > len(funcValues):
            funcValues.append(token)   

    return ' '.join(funcValues)        


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
        if NOFTblCols == 4:
            print("Tables Data Frame has correct # of columns! ")  
        elif NOFTblCols == 3:
            # add blank symbolic for each table (assuming no symbol found)
            dfIDRTables['Symbol'] = " "
        else:      
            print(dfIDRTables)
            raise InvalidTableDFException(NOFTblCols)

        # Add column headers to Data Frame
        dfIDRTables.columns = ['DB','Schema','Table','Symbol']
        #dfIDRTables.to_csv(outSQLFile, sep=',')


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
        #dfIDRCols.to_csv(outSQLFile, sep=',')

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
        bFileExists = os.path.exists(outSQLFile)
        dfSort.to_csv(outSQLFile, mode='a' if bFileExists else 'w', sep=',', index=False, header=False, columns=["Schema","Table", "ColName", "Symbol"])

    except InvalidTableDFException as ex1: 
        print(f"Exception in MergeTblAndCols: Table DF has {ex1} columns instead of 3.")

    except InvalidColsDFException as ex1: 
        print(f"Exception in MergeTblAndCols: Columns DF has {ex1} columns instead of 2.")

    except Exception as ex:
        print("Exception in MergeTblAndCols")
        print(ex.with_traceback)
        

##################
# Main
##################
inSQLFile = r'C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\HCPP\HCPP_SF_Extract_SQL.sql'

filePath = os.path.dirname(inSQLFile)
outSQLFile = os.path.join(filePath,"HCPP_Source2Target.csv")

print('*' * 10)
print(inSQLFile)
print(outSQLFile)

print("Pandas versin: "+pandas.__version__)    

processSQLFile(inSQLFile, outSQLFile)


            




      
