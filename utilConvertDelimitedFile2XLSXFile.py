########################################################################################################
# utilConvertPipeFile2CSVFile.py Parm1
#
# parm1 = filename and path to pipe-delimited file 
#
# Paul Baranoski 2025-01-09 Convert pipe-delimited file to csv file for attachments.
########################################################################################################
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import sys

infile_path=""
outfile_path=""

print("In utilConvertDelimitedFile2XLSXFile.py")
print(f"{len(sys.argv)=}")
NOFParms=(int(len(sys.argv)) - 1)
print(f'{NOFParms=}')

# sys.argv = 4 parms + 1 program name --> total 5 parms    
if NOFParms == 1:
    # module being called from shell script
    lstParms = sys.argv
    infile_path = lstParms[1]
    
    print(f"{infile_path=}")
    outfile_path = infile_path.replace('.txt','.xlsx')
    print(f"{outfile_path=}")
   
        
    try:    
        df = pd.read_csv(infile_path,sep='|') 

        df.to_excel(outfile_path,index=False)
        
        #writer = ExcelWriter('Pandas-Example2.xlsx')
        #df.to_excel(writer,'Sheet1',index=False)
        #writer.save()


    except Exception as e:
        print(e)
        sys.exit(12)
   
else:
    # module NOT called from shell script
    pass 
    
    


    
    
    



