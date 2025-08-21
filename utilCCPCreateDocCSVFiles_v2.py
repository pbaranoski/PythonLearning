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
                        processSelectStmt(arrSelectStmt)
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
                    processSelectStmt(arrSelectStmt)


    except Exception as ex:
        print("Exception occurred in function processSQLFile. ")
        print(ex.with_traceback)


def processSelectStmt(arrSelectStmt):

    #print("Start function ProcessSelectStmt ")

    arrTables = []
    arrColumns = []

    try:

        #########################################
        # Convert SELECT array into single String
        #########################################
        sSelect = ' '.join(arrSelectStmt)
        #print(sSelect)

        ################################
        # modify parameter placeholders
        ################################
        sSelect = sSelect.replace("&DBENV.","PRD")
        sSelect = sSelect.replace("$ENVNAME","PRD")
        sSelect = sSelect.replace("${ENVNAME}","PRD")

        # Remove false "FROM"s from SELECT statement
        sSelect = removeBogusFROMs(sSelect)
        #print(sSelect)

        ##############################################################
        # Remove JOIN Qualifier keywords  (to make it easier to parse)
        ##############################################################
        sSelect = sSelect.replace("INNER ","")
        sSelect = sSelect.replace("OUTER ","")
        sSelect = sSelect.replace("LEFT ","")
        sSelect = sSelect.replace("RIGHT ","")
        sSelect = sSelect.replace("CROSS ","")

        # replace multiple spaces with single space between text 
        sSelect = sSelect.strip()
        sSelect = re.sub('\\s+', ' ', sSelect)

        # init Loop variables
        idx = 0

        ################################
        # process SELECT statement
        ################################
        # find start of SELECT statement
        idxSelect = sSelect.find("SELECT ",idx)

        if idxSelect >= 0:
            idx = idxSelect

            # Find start of FROM Table statment
            idxFrom = sSelect.find(" FROM ",idx)

            # Get SELECT Columns
            arrColumns = extractCols(sSelect [idxSelect : idxFrom])
            print(arrColumns)

            # Get tables
            arrTables = extractTblNames(sSelect [idxFrom:])
            print("arrTables")
            print(arrTables)

            # Get columns from FROM/JOIN statements
            arrColumns += extractColsFromJoins(sSelect [idxFrom:])
            #arrColumns.extend(arrColumns2)
            print("arrColumns")
            print(arrColumns)

        ######################################
        # End of parsing SELECT statement
        ######################################
        print("End of parsing Select statement\n")

        ######################################
        # Create output records
        ######################################
        MergeTblAndCols(arrTables, arrColumns)

    
    except Exception as ex:
        print("Exception in function ProcessSelectStmt")
        print(ex.with_traceback)


def extractCols(sString):
    ###################################################
    # Expect that sString is "SELECT" thru "FROM table"
    ###################################################  

    arrColumns = []

    #################################################
    # Remove ' AS NAME ' from SQL String 
    # (This is so we don't pick these up as possible 
    #  column names later on).
    ##################################################                
    while True:  
        idxStart = sString.find(" AS ")
        if idxStart == -1:
            break
        # find end of 2nd token
        idxEnd = sString.find(" ", idxStart + len(" AS ") ) 
        sString = sString[:idxStart] + sString[idxEnd:]
        idxStart = idxEnd

    #################################################
    # Create separation between items to create tokens
    # to find columns.
    #################################################                
    # substr(col,1,5) --> col15
    sString = sString.replace("="," ")
    sString = sString.replace(","," ")
    sString = sString.replace("'","")
    sString = sString.replace("("," ")
    sString = sString.replace(")"," ")
    sString = sString.replace("+"," ")
    sString = sString.replace("/"," ")

    # remove multiple consecutive spaces
    sString = re.sub('\\s+', ' ', sString)

    ######################################################
    # remove embedded spaces between symbolic and col name
    # Ex: "CLEOPP. CLM_LINE_OTHR_PYR_PMT_SQNC_NUM"
    ######################################################
    if  sString.find(". ") >= 0:
        sString =  sString.replace(". ", ".")

    #################################################
    # Break string into tokens to find column names
    #################################################
    tokens = sString.split(" ")

    for token in tokens:
        # Token contains possible column name    
        if token.find(".") >= 0:

            # skip format numeric fields  --> .9999"
            if token.find(".9") >= 0:
                continue

            # skip FORMAT 'yyyymmddBHH:MI:SS.S(6)'
            if token.find("HH:MI:SS.S") >= 0:
                continue

            #print(token)
            arrColumns.append(token)

        # potential columns;      
        elif token.find("_") >= 0:
            if token.find("CURRENT_DATE") >= 0:
                continue
            elif token.find("ADD_MONTHS") >= 0:
                continue
            elif token.find("TO_DATE") >= 0:
                continue
            elif token.find("CHAR_LENGTH") >= 0:
                continue                    
            else:
                sUnknownSymbolic = "?."  
                arrColumns.append(sUnknownSymbolic+token)  
                #print(token)  

    # remove dups from list
    return list(dict.fromkeys(arrColumns)) 


def findTwoTokenLen(string, substring):
    # find end of 2nd token
    # Ex: "schema.table A "
    idx = string.find(substring)
    idx2 = string.find(substring,idx + 1)

    # Possibility that 2nd token cannot be found (end of string)
    # Ex: "TABLE ;" --> set Length to end of 1st token
    if idx2 == -1:
        idx2 = idx

    return idx2    


def extractTblNames(sString):
    ##############################################################
    # Expect String contains FROM and JOIN statements only.
    ##############################################################

    arrTableNames = []

    # remove multiple consecutive spaces
    sString = re.sub('\\s+', ' ', sString)

    ##############################################################
    # Extract Table names: Search for "FROM" 1st time.
    #                      Search for "JOIN" subsequent times.
    ##############################################################
    idx = 0
    sSearchStr = "FROM "

    while True:
        # find start of SearchStr
        idxTblStart = sString.find(sSearchStr,idx)
        
        # no more to find
        if idxTblStart == -1:
            break

        # skip past SearchStr token    
        idxTblStart += len(sSearchStr)

        # set current index      
        idx = idxTblStart

        # set current index to end of 2nd token --> Ex. "schema.table sym "
        idx += findTwoTokenLen(sString[idx:], " ")

        # Ex. "schema.table sym"
        TblAndSymbol = sString[idxTblStart:idx] 
        #print (TblAndSymbol)

        # If two tokens returned --> verify that 2nd token is symbol
        # Note: Set TblAndSymbol to Table only when no symbol exists
        tokens = TblAndSymbol.split(" ")
        if len(tokens) == 2:
            if ((sSearchStr == "FROM " and tokens[1] == "JOIN") or 
                (sSearchStr == "FROM " and tokens[1] == "WHERE") or 
                (sSearchStr == "JOIN " and tokens[1] == "ON")):
                TblAndSymbol = tokens[0]
        elif len(tokens) == 1:
            # there was only one token to be found; no symbolic for table
            pass

        #print (TblAndSymbol)

        arrTableNames.append(TblAndSymbol)

        # Search for JOIN Statements after initial FROM 
        sSearchStr = "JOIN "

    ##############################################################
    # return list of Tables
    ##############################################################
    return arrTableNames

def extractColsFromJoins(sString):

    ##############################################################
    # Expect String contains FROM/JOIN statements only.
    ##############################################################
    arrColNames = []

    #################################################
    # Create separation between items to create tokens
    # to find columns.
    #################################################                
    sString = sString.replace("="," ")
    sString = sString.replace("+"," ")
    sString = sString.replace("/"," ")
    sString = sString.replace("("," ")
    sString = sString.replace(")"," ")

    # remove multiple consecutive spaces
    sString = re.sub('\\s+', ' ', sString)

    ################################################################
    # Note: Will skip FROM statement; 
    #       Process each JOIN skipping table name and looking for
    #       Columns used in join conditions  
    ################################################################
    # Find first JOIN
    idx = sString.find(" JOIN ",0) 

    if idx >= 0:

        while True:

            # Skip JOIN token
            idx += len(" JOIN ")

            # find start of Str JOIN condition
            idxStart = sString.find("ON ",idx)

            # find end of current JOIN conditions (Start of next JOIN)
            idxEnd = sString.find(" JOIN ",idx)

            # Adjust idx to point to next JOIN 
            idx = idxEnd

            # Split JOIN conditions into tokens
            if idxEnd >= 0:
                tokens = sString[idxStart : idxEnd].split(" ")
            else:    
                tokens = sString[idxStart : ].split(" ")

            for token in tokens:
                if token.find("_") >= 0:
                    arrColNames.append(token)

            # no more JOINS to find
            if idxEnd == -1:
                break

    ##############################################################
    # Process WHERE and/or GROUP BY
    ##############################################################
    idx = sString.find(" WHERE ",0) 
    if idx == -1:
        idx = sString.find(" GROUP BY ",0) 

    if idx >= 0:
        tokens = sString[idx : ].split(" ")

        for token in tokens:
            if token.find("_") >= 0:
                arrColNames.append(token)       

    ##############################################################
    # return list of Tables
    ##############################################################
    return arrColNames


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
        outSQLFile = inSQLFile.replace(".txt",".csv")
        out_file = os.path.join(os.path.join(out_dir,projDirBase), outSQLFile)

        print('*' * 10)
        print(in_file)
        print(out_file)
        processSQLFile(in_file, out_file)

print("Pandas versin: "+pandas.__version__)    



            




      
