# PythonTest2

import os
import re

# Function for natural sorting of input file names so files are processed in numerical order
# Paul --> this is over-kill.  if filenames have similar format, they will naturally sort in correct order
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    print ("alphanum_key_s: "+s)
    print(str(re.split('([0-9]+)', s)))
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

#['C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\InfolderPath\\file', '4', '.txt']
#alphanum_key_s: C:\Users\user\Documents\PythonLearning\LandingDir\InfolderPath\file3.txt   
#['C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\InfolderPath\\file', '3', '.txt']
#alphanum_key_s: C:\Users\user\Documents\PythonLearning\LandingDir\InfolderPath\file2.txt   
#['C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\InfolderPath\\file', '2', '.txt']
#alphanum_key_s: C:\Users\user\Documents\PythonLearning\LandingDir\InfolderPath\file1.txt
#['C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\InfolderPath\\file', '1', '.txt']

##################################################
# test input mappings array
##################################################
input_mappings = {"Address": "ADDRESS",
                   "Neighborhood":"<None>",
                   "City":"CITY",
                   "Region" : "REGION",
                   "Postal" : "POSTAL",
                   "PostalExt": "POSTALEXT"
                  }


#for field in input_mappings:
#    print ("field: "+field)
#    print ("input_mappings: "+input_mappings[field])


##################################################
# test input mappings array
##################################################
in_csvlist = "C:/Users/user/Documents/PythonLearning/LandingDir/InfolderPath/csvlist.txt"

with open(in_csvlist) as csvlist_obj:
    csvlist = csvlist_obj.readlines()
    csvlist = [i.strip("\n") for i in csvlist]
orig_files = [f for f in csvlist if os.path.exists(f)]
#print ("orig_files: "+str(orig_files))

#orig_files.sort(key=alphanum_key)

if len(orig_files) == 0:
    print(". Quitting program.")
    exit(0)

## sort method sorts the strings in ascending sequence. 
## Why the more difficult method to sorting? If there are sequence numbers in the filenames
## the files will sort in proper order anyway.
print ("before Paul sort")
orig_files.sort()  
print ("orig_files: "+str([f for f in orig_files])) 

#print("before geo sort")
#print ("geo sort: "+ str([f for f in orig_files]))  

 