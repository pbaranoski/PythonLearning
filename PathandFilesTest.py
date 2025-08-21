from pathlib import Path
import os

#in_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCR documentation\FinalOutFiles"
in_dir = r"C:\Users\user\OneDrive - Apprio, Inc\Documents\Sprints\CCR documentation\InFiles"


# Get list of Project directories (i.e., BLUE_BUTTON, PECOS)
#for projDirBase in (projDirBase for projDirBase in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir,projDirBase)) ):
#    print (projDirBase)

# Get directory
path = Path(in_dir)
print("current Path: "+str(path))

#for filename in path.glob("*.*"):
#for filename in path.glob("*.py*"):
for fileOrDir in path.glob("*"):
    if os.path.isdir(fileOrDir):
        print (fileOrDir)
