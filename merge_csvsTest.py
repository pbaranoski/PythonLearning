import os
import pandas
import traceback
import csv

#in_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\FID_file1_txt.csv"
#out_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\FIDfile1_txt.csv"
in_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input\\InPaul.csv"
out_csv = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_output\\OutPaul.csv"


# Function to merge the output geocoded fields with input csv and drop FID column
def merge_csvs(out_csv, in_csv):
    # processed_lines_log = os.path.join(log_dir, "processed_lines.csv")
    # in_file = os.path.join(log_dir, "infile.csv")
    # out_file = os.path.join(log_dir, "outfile.csv")
    # skipped_lines_log = os.path.join(log_dir, "skipped_lines.csv")

    # with open(processed_lines_log, 'w') as fp:
    try:
        dtype_dict = {"POSTAL": str, "POSTALEXT": str}
        ## Paul read entire in_csv and out_csv file into in_df and out_df.
        ## Paul the dtype=dtype_dict tells the pandas.read_csv to treat the Postal/zip codes as strings 
        #  and not numbers.      
        out_df = pandas.read_csv(out_csv,sep = "\t", na_filter=False, warn_bad_lines=True, error_bad_lines=False)
        in_df = pandas.read_csv(in_csv, dtype = dtype_dict, na_filter=False, warn_bad_lines=True, error_bad_lines=False)
    
        # Created new merged path/filename based on the out_csv filename, but removing the "FID" text.
        merged_csv = out_csv.replace("FID","")

        out_df = out_df.merge(in_df)     # Getting Error Message Here before fixing after ArcGIS 10.8 upgrade
        out_df = out_df.drop("FID",1)
        #workaround for quoting issue, pandas df treats POSTALEXT as numeric so expllicity converting to string
        fields = ["SCORE", "DISPLAYX", "DISPLAYY", "POSTALEXT"]
        for cols in out_df:
            if cols in fields:
                out_df[cols] = out_df[cols].astype(str)

        out_df.to_csv(merged_csv,sep = "\t", index=False, line_terminator = "\n", quoting=csv.QUOTE_NONNUMERIC)

        return merged_csv
    except:
        print (traceback.format_exc())


dtype_dict = {"POSTAL": str, "POSTALEXT": str}

out_df = pandas.read_csv(out_csv,sep = ",", na_filter=False, warn_bad_lines=True, error_bad_lines=False)
in_df = pandas.read_csv(in_csv, dtype = dtype_dict, na_filter=False, warn_bad_lines=True, error_bad_lines=False)

# Created new merged path/filename based on the out_csv filename, but removing the "FID" text.
merged_csv = out_csv.replace("OutPaul","OutPaulMerged")

#out_df = out_df.merge(in_df,on=["FID"]) 
out_df = out_df.merge(in_df)     
#out_df = out_df.drop("FID",1)

out_df.to_csv(merged_csv,sep = "\t", index=False, line_terminator = "\n", quoting=csv.QUOTE_NONNUMERIC)
