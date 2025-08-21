import sys
import os
import pandas as pand

Source2TargetCSV = r"C:\Users\user\Documents\BlueButtonSourceToTarget_Layout.csv"
FBFile = r"C:/Users/user/Documents/blbtn_clm_ext.txt"
CSVFile = r"C:/Users/user/Documents/blbtn_clm_ext.csv"
txtDelimiter=","

def createCSVFile():

    #################################################
    # Read Source2Target mapping csv file.
    # File should have 3 columns: 
    #    1) column name
    #    2) start position
    #    3) end position
    #################################################
    dfSource2Target = pand.read_csv(Source2TargetCSV, dtype=str, na_filter=False) 

    # Force 1st colum to be "Extract Field Name"
    dfSource2Target.set_axis(['Extract Field Name','StartPos','EndPos'], axis='columns', inplace = True)

    # Extract list of column names from Data Frame
    col_names = dfSource2Target['Extract Field Name'].tolist()
    #for col in col_names:
    #    print(col)

    # Remove column of column names from Data Frame
    # Convert StartPos and EndPos into list of records.
    dfSource2Target.drop('Extract Field Name', axis=1, inplace=True)
    recs = dfSource2Target.to_records(index=False)
    
    ##################################################
    # Convert column offsets into new list of tuples.
    ##################################################
    col_specs = []

    for start, end in recs:
        new_start = int(start) - 1
        new_end = int(end)
        new_tuple = (new_start, new_end)
        col_specs.append(new_tuple)
        #print(start)
        #print(end)

    #for col in col_specs:
    #    print(col)
    print(col_names)
    print (col_specs)

    ##############################################
    # Create new DataFrame using Fixed-width file. 
    #############################################
    fwDF = pand.read_fwf(FBFile, dtype=str, names=col_names, header=None, colspecs=col_specs)
    #print("Number of rows in FW file: " + str(len(fwDF.index)))
    
    #for i in fwDF.columns:
    #    if fwDF[i].dtype == 'object':
    #        fwDF[i] = fwDF[i].str.replace(' ', '')
    #        fwDF[i] = fwDF[i].str.rstrip(' ')    
    #    else:
    #        pass

    ##############################################
    # Convert DataFrame from Fixed-width file into
    #  CSV file. 
    #############################################
    print(f"txtDelimiter:{txtDelimiter}")
    fwDF.to_csv(CSVFile, index=False, sep=txtDelimiter)

    #print("Complete!")


if __name__ == "__main__":
    createCSVFile()