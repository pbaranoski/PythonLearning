import os

temp_dir = "C:\\Users\\user\\Documents\\PythonLearning\\LandingDir\\temp_input"

def get_file_recordcount(in_file):
    with open(in_file,"r") as fobj:
        # why do we substract 1 in Geo program?  
        # Are we taking into account header?
        count = len(fobj.readlines())-1
    return count

temp_files = os.listdir(temp_dir)

for f in temp_files:
    fp = os.path.join(temp_dir,f)
    print("filename: "+fp)
    print()
    count = get_file_recordcount(fp)
    print("File {} contains {} records".format(f, str(count)))
