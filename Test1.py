import os
import sys
import smtplib
import sys
import re

os.environ["HOME"] = "/home/user2"
os.environ["PYTHON_ERROR_MSG"] = "Big Trouble in Paradise"


print (f"{os.getenv('PYTHON_ERROR_MSG')}" )


infile_path="/app/IDRC/XTR/CMS/data/DashboardVolRptData_2024_CY_20250108.144617.txt"
outfile_path="/app/IDRC/XTR/CMS/data/DashboardVolRptData_2024_CY_20250108.144617.csv"

print(f"{infile_path=}")
outfile_path = infile_path.replace('.txt','.csv')
print(f"{outfile_path=}")

sys.exit(0)
#For a 10 digit NDC in the 4-4-2 format, add a 0 in the 1st position.
#For a 10 digit NDC in the 5-3-2 format, add a 0 in the 6th position.
#For a 10 digit NDC in the 5-4-1 format, add a 0 in the 10th position.

"""
p_4_4_2 = re.compile("^[0-9]{4}-[0-9]{4}-[0-9]{2}$")
p_5_3_2 = re.compile("^[0-9]{5}-[0-9]{3}-[0-9]{2}$")
p_5_4_1 = re.compile("^[0-9]{5}-[0-9]{4}-[0-9]{1}$")

p_5_4_2 = re.compile("^[0-9]{5}-[0-9]{4}-[0-9]{2}$")
p_11 = re.compile("^[0-9]{11}$")

#sNDC = "3456-4567-23"
#sNDC = "03456-567-23"
#sNDC = "03456-6567-3"
sNDC = "69639-103-01"  #69639-0103-01
sNDC = "69639010301"
sNDC = "69639-0103-01"

if (p_4_4_2.match(sNDC)):
    sNDC_11 = '0' + sNDC
elif (p_5_3_2.match(sNDC)):    
    sNDC_11 = sNDC[0:6] + '0' + sNDC[6:]
elif (p_5_4_1.match(sNDC)):    
    sNDC_11 = sNDC[0:11] + '0' + sNDC[11:]
elif (p_5_4_2.match(sNDC)):  
    print("This is a valid NDC") 
    sNDC_11 = sNDC
elif (p_11.match(sNDC)):   
    sNDC_11 = sNDC[0:5]+ '-' + sNDC[5:9] + '-' + sNDC[9:]    
else:
    print ("invalid NDC")


print (sNDC_11)
"""

iTotNOFFiles = 0
iMaxNOFFiles=35
iTotFileSize = 0
File2Include_Size=33737017870
iMaxSizeFiles=4294967296

if   ((iTotNOFFiles + 1)  > iMaxNOFFiles):  

    print("Fail")
else:
    print("success")


if (  ((iTotNOFFiles + 1)  > iMaxNOFFiles) or 
    
        ((iTotFileSize + File2Include_Size) > iMaxSizeFiles) ):

    print("Fail")
else:
    print("success")   

sys.exit(0)

IDR_CLM_TYPE_CD : str = '01234'  # input file clm_type_cd is 5 bytes.
IDR_CLM_HIC_NUM : str  = '123456789A'
IDR_BENE_ID_TYPE_CD : str = '88'
IDR_BENE_MBI_ID   = "123456789012"


sOutputRecFixed = ( 


                       # REC_KEY +
	                    ('0' * 5) +  # REC_LENGTH_CNT [5];  // PIC S9(5) COMP-3.

	                    (' ' * 1) + # H_FILLER_1 [1]     
	                    IDR_CLM_TYPE_CD [1:5] +   # input file clm_type_cd is 5 bytes.
                        IDR_CLM_HIC_NUM  + 
                        IDR_BENE_ID_TYPE_CD + 
                        IDR_BENE_MBI_ID   

) 
print(f"{sOutputRecFixed=}")        

sys.exit(0)

lstIDR_CLM_DGNS_R_CD = []
lstIDR_CLM_DGNS_R_CD.append('MD')
lstIDR_CLM_DGNS_R_CD.append('DE')
lstIDR_CLM_DGNS_R_CD.append('AZ')

for i in range(0,2):
    print(f"{lstIDR_CLM_DGNS_R_CD[i]}")


for DGNS_R_CD in lstIDR_CLM_DGNS_R_CD:
    print (f"{DGNS_R_CD}")

sString : str = ""

sString += ' '
sString += "hi "
sString +=  " World"
print (f"{sString=}")

sys.exit(0)

lRecLenCount = 857

sRecLenCountFormatted = format(lRecLenCount, "0>5") 
print (f"sRecLenCountFormatted:{sRecLenCountFormatted}")


sString = "0123456789abcdefghij"
encoded=sString.encode('utf-8')
baBytes=bytearray(encoded)

baBytes2 = bytearray(sString.encode('utf-8'))

baBytes[3] = int("X")

sString = baBytes.decode()

print(f"sString:{sString}")


#res = test_string.encode('utf-8')