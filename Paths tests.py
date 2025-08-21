import os
import sys

temp_dir = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input"

def get_file_recordcount(in_file):
    with open(in_file,"r") as fobj:
        # why do we substract 1 in Geo program?  
        # Are we taking into account header?
        # len is length/count of array members
        count = len(fobj.readlines())-1
    return count

# one way to get list of files in directory
with os.scandir(temp_dir) as files:
    for fl in files:
        print(fl.name)
 
# 2nd way to get list of files/sub-dirs in directory
temp_files = os.listdir(temp_dir)
for f in temp_files:
    fp = os.path.join(temp_dir,f)
    if os.path.isfile(f):
        print("filename: "+fp)
        print()
        count = get_file_recordcount(fp)
        print("file "+f + " contains "+str(count)+" records.")

print()
print("os.walk method")
for curpath, dirs, files in os.walk(temp_dir, topdown=True):
    for dir in dirs:
        print("dirs: {}".format(str(dir)))

    for f in files:
        print("files: {}".format(str(f)))
