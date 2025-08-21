import os
import pandas
import traceback
import csv

#in_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\FID_file1_txt.csv"
#out_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\FIDfile1_txt.csv"
in_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\InPaul.csv"
out_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\OutPaul.csv"


dtype_dict = {"POSTAL": str, "POSTALEXT": str}

out_df = pandas.read_csv(out_csv,sep = ",", na_filter=False, warn_bad_lines=True, error_bad_lines=False)
in_df = pandas.read_csv(in_csv, dtype = dtype_dict, na_filter=False, warn_bad_lines=True, error_bad_lines=False)

# Created new merged path/filename based on the out_csv filename, but removing the "FID" text.
merged_csv = out_csv.replace("OutPaul","OutPaulMerged")
#merged_csv = out_csv.replace("OutPaulTabbed","OutPaulTabbedMerged")

## Paul --> you can specify a key
out_df = out_df.merge(in_df, on="FID")    
## Paul --> what the geo code looks like.  Doesn't specify a key.
#out_df = out_df.merge(in_df) 

# Paul --> drop the first column after merge (the key)
#out_df = out_df.drop("FID",1)

out_df.to_csv(merged_csv,sep = "\t", index=False, line_terminator = "\n", quoting=csv.QUOTE_NONNUMERIC)
