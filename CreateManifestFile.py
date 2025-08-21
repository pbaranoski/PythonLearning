###################################################################################
#
# Run `python3 CreateManifestFile.py -h` for more info.
###################################################################################
# 10/13/2022 Paul Baranoski  Created program.  
#
############################################################
import os
import sys
import json
import argparse
import logging


dctContactInfo = {
    "fullName": "fullName", 
    "phoneNumber": "phoneNumber",
    "email": "email"

}

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple

    return str(amount) + suffix


def BuildManifestFile():

    ###############################################
    # Get parameters
    ###############################################
    try:    
        parser = argparse.ArgumentParser(description="S3 file combiner")
        parser.add_argument("--bucket", help="S3 bucket")
        parser.add_argument("--folder", help="S3 folder")
        parser.add_argument("--files", help="S3 files")
        parser.add_argument("--REmails", help="Recipient email addresses")
        parser.add_argument("--filesize", type=int, help="total filesize of S3 files")
        parser.add_argument("--filename", help="Manifest Path and filename")

        args = parser.parse_args()
        print(f"args: {args}")

        #sFileNames = args.files
        sFileNames = "Mickey.txt,Donald.jpg,Rigby.txt,Bugs.csv.gz,".replace(',',' ').strip()
        lstFileNames = sFileNames.split(" ")
        nofFiles = len(lstFileNames)
        #print(nofFiles)

        #sFileLocation = args.folder
        sFileLocation = "xtr/DEV/Blbtn"

        #dataRecepientEmails = args.REmails
        dataRecepientEmails = "pbaranoski@apprioinc.com,jturner@apprioinc.com,SGayam@apprioinc.com"

        #iFileSize = args.filesize
        iFileSize=5034556

        #print(pretty_size(iFileSize))
        lstFileSizeInfo = pretty_size(iFileSize).split(' ')
        print(f"lstFileSizeInfo: {lstFileSizeInfo}")

        totFileSize = lstFileSizeInfo[0]
        totFileSizeUnit = lstFileSizeInfo[1]
        #print( totFileSizeUnit)

        #sFilePathAndName = args.filename  
        sFilePathAndName = os.path.join(os.getcwd(),"manifestFile.man")

        ###############################################
        # Build List of Filename Dictionary items
        ###############################################
        print("Build S3 Filename Dictionary items")
        lstDictS3Filenames = [{"fileName": sFileName, "fileLocation": sFileLocation} for sFileName in lstFileNames]    
        #print(lstDictS3Filenames)

        ###############################################
        # Build Share Detail Dictionary
        ###############################################
        dctShareDetails = { "dataRequestID" : "dataRequestID",
                            "shareduration" : 1,
                            "dataRecepientEmails" : dataRecepientEmails, 
                            "totalNumberOfFiles"  : nofFiles,
                            "totalExtractFileSize" : totFileSize,
                            "totalExtractFileSizeUnit" : totFileSizeUnit
        }

        ###############################################
        # Build Manifest file Dictionary
        ###############################################
        dctManifest = {"fileInformation": lstDictS3Filenames,
                "ShareDetails": dctShareDetails ,
                "requestorContactInfo": dctContactInfo,
                "comments" : "Mickey Mouse loves Minnie!"  
                }  

        ###############################################
        # Write out manifest json file
        ###############################################
        print("Convert dictionary to json format")

        json_obj = json.dumps(dctManifest, indent=4)
        print(json_obj)

        print("Write manifest file")
        with open(sFilePathAndName, "w+") as manFile:
            manFile.writelines(json_obj)


    except Exception as e:
        logging.error("Exception occured in combinedS3Files.py.")
        print(e)

        sys.exit(12) 

    ###############################################
    # write output manifest file
    ###############################################
    sys.exit(0)


if __name__ == "__main__":
    BuildManifestFile()

