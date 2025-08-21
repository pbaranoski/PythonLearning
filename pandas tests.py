import pandas as pd
import numpy 
import sys
import csv
import os
import datetime
#import json
import matplotlib.pyplot as plt


class geoCodeEvent(object):

    spacer = "  "

    def __init__(self, infile="", infile_cnt=0, infile_clean="", infile_clean_cnt=0, outfile="", outfile_cnt = 0, start_time=None, end_time=None):
        self.infile = infile
        self.infile_cnt = infile_cnt
        self.infile_clean = infile_clean
        self.infile_clean_cnt = infile_clean_cnt
        self.outfile = outfile
        self.outfile_cnt = outfile_cnt
        self.start_time = start_time
        self.end_time = end_time

    def elapsedTime(self):
        return self.end_time - self.start_time 

    def countDiff(self):
        diff =  self.infile_cnt - self.outfile_cnt
        return diff
        #return (date(self.infile_cnt - self.outfile_cnt)).strftime("%H:%M:%S")   

    def displayReportRec(self):
        rec = self.infile.ljust(15," ") 
        rec = rec + self.spacer
        rec = rec + str(self.infile_cnt).rjust(8," ")
        rec = rec + self.spacer
        rec = rec + self.infile_clean.ljust(20," ")
        rec = rec + self.spacer
        rec = rec + str(self.infile_clean_cnt).rjust(8," ") 
        rec = rec + self.spacer
        rec = rec + self.outfile.ljust(20," ")
        rec = rec + self.spacer
        rec = rec + str(self.outfile_cnt).rjust(8," ") 
        rec = rec + self.spacer
        rec = rec + str(self.elapsedTime()).rjust(12," ")
        return rec

    def displayReportHdr(self):
        rec = "Input File".ljust(15," ") 
        rec = rec + self.spacer
        rec = rec + "NOF Recs".ljust(8," ")
        rec = rec + self.spacer
        rec = rec + "Clean Input File".ljust(20," ")
        rec = rec + self.spacer
        rec = rec + "NOF Recs".ljust(8," ") 
        rec = rec + self.spacer
        rec = rec + "Output File".ljust(20," ")
        rec = rec + self.spacer
        rec = rec + "NOF Recs".ljust(8," ") 
        rec = rec + self.spacer
        rec = rec + "Elapsed Time".ljust(12," ")
        return rec        

log_dir = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\logs\\"
in_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\InPaul.csv"
out_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\OutPaul.csv"
in_cleaned_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\InPaulCleansed.csv"

skipped_file = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\skipped.csv"
bad_delm_file = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\badDelimters.csv"
in_json = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\Example.json"
in_json2 = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\Example2.json"

valid_num_delimiters = 6
delimiter = ","

surname = "Mulligan"
print(f"here we go again {surname}!")
#*****\/******
logdate = datetime.datetime.now()
log_file = "GeoProcessSumrylog_"+logdate.strftime("%Y-%m-%d %H-%M-%S"+".txt")
print(log_file)
Smry_log_file = os.path.join(log_dir,"GeoProcessSumrylog_"+logdate.strftime("%Y-%m-%d %H-%M-%S"+".txt"))
print(Smry_log_file)
fSmryLog = open(Smry_log_file,'w')

def write_summary_log(msg):

    metric.start_time = datetime.datetime.now()
    metric.infile_cnt = 87
    metric.end_time = datetime.datetime.now()

    date = datetime.datetime.now()
    time_stamp = date.strftime("%Y-%m-%d %H:%M:%S")
    
    smry_log_msg = "{} {}".format(time_stamp, msg)
    fSmryLog.write(smry_log_msg+"\n")

#*****/\******
#write_summary_log("Program {} started.".format(os.path.basename(sys.argv[0])))
metric = geoCodeEvent()

write_summary_log("Program started")
write_summary_log("Another thing happened")
write_summary_log("Message::Failed[{}]".format(0))

print(metric.infile_cnt)
print(metric.start_time)

print("Pandas version: "+pd.__version__)
#print("Pandas dependency versions: "+pd.show_versions())

original_file = os.path.basename(in_cleaned_csv)[:-4] + "_BadDelim.txt"
original_file = in_cleaned_csv[:-4] + "_BadDelim.txt"
print(original_file)

string = "This is a long\t string with\t tabs\t"

print("NOF tabs: "+str(string.count("\t",1)))
rec_num = 88
count = 5
msg = "Skipping line {} expected {} saw {}".format(rec_num,valid_num_delimiters, count)
print(msg)  

#*************************************
#*
#*************************************
with open(in_csv, 'r') as ifp1, open(in_cleaned_csv, 'w') as ifp2, open(bad_delm_file, 'w') as ofp1:
  infile = ifp1.readlines()
  for rec in infile:
    # rec contains a '\n' at the end of the record
    #print("NOF lf:"+str(rec.count("\n",1)))

    count = rec.count(delimiter)

    # to print string w/o adding newline character
    #print(rec, end='')

    # write statement requires programmer add newline char; unless newline is already part of string
    if count == valid_num_delimiters:
      ifp2.write(rec)
    else:
      ofp1.write(rec)
      print ("rec has incorrect # delimiters:"+ rec) 


#######################################################################
# test 12: merge test of two DF
#######################################################################
indf = pd.read_csv(in_csv)
outdf = pd.read_csv(out_csv)

# this works like an INNER JOIN
#joindf = indf.merge(outdf)  #--> works like inner JOIN
joindf = indf.merge(outdf, left_on="FID", right_on="FID", how="left")
#joindf = indf.merge(outdf, left_on="FID", right_on="FID", how="right")
#joindf = indf.merge(outdf, left_on="FID", right_on="FID", how="outer")
#joindf = indf.merge(outdf, how="cross")

#print (joindf)

  # force column to be null
  ##for i in joindf.index:
  ##  joindf.loc[i, "FLD6"] = numpy.NaN
  ##
  ##print(joindf)

print("we are here")
# Find rows with null in a specific column
#missing = joindf.loc[joindf["FLD6"].isnull()]
missing = joindf.loc[joindf["FLD5"].isnull()]
inner = joindf.loc[joindf["FLD5"].notnull()]

print("tony")
print(inner)
print("end tony")

if missing.empty == False:
  print("missing has some rows that were not matched.")
  print(missing)

  # Need the "newline='' to prevent creating an extra \r from being added to end of record"
  #with open(skipped_file, 'w') as fp1:
  #with open(skipped_file, 'w', newline='') as fp1:
  with open(skipped_file, 'wb') as fp1:    
    missing.to_csv(fp1, sep='\t', index=False,quoting=csv.QUOTE_ALL)
    fp1.close()
else:
  print("no mismatches")

sys.exit(0)

#for i in joindf.index:
#  if joindf.loc[i, "FLD6"] < 12 or joindf.loc[i, "COUNT"] > 100: 
#     print("Column is null") 
#     joindf.drop(i,inplace=True)

#print (joindf)

sys.exit(0)

#######################################################################
# test 14: iterating
#######################################################################
indf = pd.read_csv(in_csv)

##row = indf.itertuples
##for row in indf.itertuples(index=False):
##  print("newrow: "+ str(row))

##newdf = indf["FLD3"]
##print(newdf)
##print(newdf.iteritems)

# col/row pairs. This only prints column names
##for x,y in indf.iteritems():
##  print(x)

for x in indf.index:
  if indf.loc[x, "COUNT"] > 50:
    print(indf.loc[x])

sys.exit(0)

#######################################################################
# test 13: combining columns of data frame joins
#######################################################################
indf = pd.read_csv(in_csv)
outdf = pd.read_csv(out_csv)

#newdf = indf.groupby(['FLD2']).sum()
#newdf = indf.groupby(['FLD2']).max()
#newdf = indf.groupby(['FLD2']).min()
newdf = indf.groupby(['FLD2']).count()
#newdf = indf.pop("FLD3")  --> remove FLD3 from indf, but returns that column

print (newdf)
print(indf)

sys.exit(0)

#######################################################################
# test 12: merge test of two DF
#######################################################################
indf = pd.read_csv(in_csv)
outdf = pd.read_csv(out_csv)

# this works like an INNER JOIN
joindf = indf.merge(outdf)  #--> works like inner JOIN
#joindf = indf.merge(outdf, left_on="FID", right_on="FID", how="left")
#joindf = indf.merge(outdf, left_on="FID", right_on="FID", how="right")
#joindf = indf.merge(outdf, left_on="FID", right_on="FID", how="outer")
#joindf = indf.merge(outdf, how="cross")

print (joindf)

sys.exit(0)

#######################################################################
# test 11: join two DF that are not identical
#######################################################################
indf = pd.read_csv(in_csv)
outdf = pd.read_csv(out_csv)

# default is left join
joindf = indf.set_index("FID").join(outdf.set_index("FID"), lsuffix="L", rsuffix="R")
#joindf = indf.set_index("FID").join(outdf.set_index("FID"), lsuffix="L", rsuffix="R", how="inner")
# outdf is left "table"; indf is right "table"
#joindf = indf.set_index("FID").join(outdf.set_index("FID"), lsuffix="L", rsuffix="R", how="left")
#joindf = indf.set_index("FID").join(outdf.set_index("FID"), lsuffix="L", rsuffix="R", how="right")
#joindf = indf.set_index("FID").join(outdf.set_index("FID"), lsuffix="L", rsuffix="R", how="outer")

# get 1st row in df
#print(joindf.iloc[0])

print(joindf)
##print(joindf.dtypes)  --> show data types of columns; mixed types will display "object"
##Get list of indices
##print(joindf.index)
##print(joindf.columns)
#print(joindf.info(verbose=True))
#print(joindf.describe)
#df.select_dtypes(include=['float64'])
#print(joindf.size) --> # of total cells (rows x cols)
#print(joindf.memory_usage())
#print(joindf.head(2))
#print(joindf.count()) --> count number of non-null values for each column

#joindf["COUNT"] = 0  --> assign all rows values for column = 0
##joindf.fillna({"COUNT":0}, inplace=True)
##print(joindf.astype({'COUNT': 'int32'}).dtypes)

#if joindf.empty:
#    print("Running on Empty")
#else:
#    print("Full tank of gas")

sys.exit(0)

#######################################################################
# test 10: join two DF that are identical
#######################################################################
df = pd.read_csv(in_csv)
newdf = df.copy()
# Assign row 14, column FLD1 a specific value
df.loc[14,"FLD1"] = "BONUS TEXT"
##print(df)

diffdf = df.compare(newdf)
##print(diffdf)

joindf = df.set_index("FID").join(newdf.set_index("FID"), lsuffix="leftBrain", rsuffix="rightBrain")
joindf.drop(columns=["FLD1leftBrain","FLD2leftBrain","FLD3leftBrain"], inplace=True)

# joindr.at[row, col]
# extract only two columns from data frame; syntax loc[rows: columns]
subdf = joindf.loc[:, ["FLD1rightBrain", "COUNTrightBrain" ]]
#(subset=["FLD2leftBrain"], inplace=True)   
print(joindf)
print (subdf)

sys.exit(0)

#######################################################################
# test 9: plotting graphs
#######################################################################
df = pd.read_csv(in_csv)
df["COUNT"].fillna(0, inplace=True)
df.fillna("",inplace=True)
df.drop_duplicates(inplace=True)

#df.plot()
#df.plot(kind = "scatter", x = "FID", y = "COUNT")
#df.plot(kind = "hist", x = "COUNT")
df["COUNT"].plot(kind="hist")
plt.show()

sys.exit(0)

#######################################################################
# test 8: cleaning data -> validating data
#######################################################################
df = pd.read_csv(in_csv)
# count # of non-null columns in df
#print(df.count())

df["COUNT"].fillna(0, inplace=True)
df.fillna("",inplace=True)
#print(df.count())

for i in df.index:
  if df.loc[i, "COUNT"] < 12 or df.loc[i, "COUNT"] > 100: 
    df.loc[i, "COUNT"] =  "*"
    #df.drop(i,inplace=True)

#print(df)
# prints true or false
print(df.duplicated())

# The (inplace = True) will make sure that the method does NOT return a new DataFrame, 
# but it will remove all duplicates from the original DataFrame.
df.drop_duplicates(inplace=True)
print (df)

sys.exit(0)


#######################################################################
# test 7: cleaning data -> replacing nulls; format dates; dropping bad data rows
#######################################################################
df = pd.read_csv(in_csv)

# anything done to df is also done to new_df
new_df = df
# instead do this to have an independent copy
new_df = df.copy

#new_df = df.dropna()
#print(new_df.to_string)

#print()
#df.dropna(inplace=True)
#print(df.to_string)

#print()
#df.fillna("888",inplace=True)
#print(df)
print()
x = df["COUNT"].mean()
y = df["COUNT"].median()
print(x)
print(y)
df["COUNT"].fillna(x, inplace=True)

df.dropna(subset=["Date_FLD"], inplace=True)

df["Date_FLD"] = pd.to_datetime(df["Date_FLD"])
print(df)


#print()
#new_df["Date_FLD"].fillna("888", inplace=True)
#new_df["COUNT"].fillna("777", inplace=True)
#print(new_df)

sys.exit(0)

#############################################################
# test 6: JSON files (key/value pairs)
#############################################################
# can only be used for single json structure
df = pd.read_json(in_json2)
print(df)

# can read mixed json structure 
##with open(in_json, "r") as read_file:
##    data = json.load(read_file)
##print (data)

#############################################################
# test 5: Load files into Data Frames
#############################################################
df = pd.read_csv(in_csv)

# printing a data frame will only print the first 5 rows and the last 5 rows
#print (df)
print()
print(df.to_string)

df = pd.read_csv(in_csv)

print(df.head(3))
#print(df.tail(3))

# tail w/o number defaults to 5 lines
print(df.tail())

#############################################################
# test 4: Data Frames
#############################################################
myDS2 = {
    'Player':["Mullins", "Mancini","Mountcastle"],
    'RBIs':[34, 57, 43],
    'HRs':[16, 15, 14]
}

# pd is an alias for pandas.  import pandas as pd
df = pd.DataFrame(myDS2,index=["player1","player2","player3"])
print(df)

print()
print("index entry 0")
var = df.loc["player1"]
#var = df.loc[0]
print(var)

#############################################################
# test 3: Series / Dictionary (instead of zero-based index; String-based)
#############################################################
calories = {"day1": 420, "day2": 380, "day3": 390}
months = {"JAN": "January ", "FEB": "February", "MAR": "March   "}

myvar = pd.Series(months)
myvar2 = pd.Series(months, index = ["MAR", "FEB"])

print(myvar)
print(myvar2)

#############################################################
# test 2: Series
#############################################################
months = ["January", "February", "March"]
abrevs = ["JAN","FEB","MAR"]

var = pd.Series(months)
myvar = pd.Series(months, index = abrevs)

print ("print month using ABR as index: "+ myvar["MAR"])
print ()

print ("Months:")
print (pd.Series(months))
print ("-----")
print (var)
print()
# below produce the same results
print ("1st series months: "+months[0])
print ("1st series var: "+var[0])

print ()

#############################################################
# test 1: dataframe: multi-dimension table
#############################################################
mydataset = {
  'languages': ["COBOL", "REXX", "MVS Assemble", "java", "python", "C", "C++", "C#"],
  'RDBMS':["DB2", "Oracle", "SQL Server", "MS Access", "MySQL", "PostgreSQL", "Teradata", "MariaDB"]
}

myDS2 = {
    'Player':["Mullins", "Mancini","Mountcastle"],
    'RBIs':[34, 57, 43],
    'HRs':[16, 15, 14]
}

# pd is an alias for pandas.  import pandas as pd
myvar = pd.DataFrame(mydataset)
myvar2 = pd.DataFrame(myDS2)

print("Pandas version: "+pd.__version__)
print() 
print(myvar2)
#print() 
#print(myvar)

