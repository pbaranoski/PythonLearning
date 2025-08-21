import boto3
import os
import argparse
import logging
import sys


def new_s3_client():
    # initialize an S3 client with a private session so that multithreading
    # doesn't cause issues with the client's internal state
    session = boto3.session.Session()
    return session.client('s3')


def _list_all_objects_with_size(s3, folder):

    ##########################################################
    # Response contains Dictionary with item "Contents"
    # Within "Contents is a list that contains Dictionary 
    # The "Contents" dictionary contains keys: Key, Size,
    #     LastModified, ETag, StorageClass
    # 1) return tuple  2) return Dictionary
    ##########################################################
    def resp_to_filelist(resp):
        #return [(x['Key'], x['Size']) for x in resp['Contents']]
        return [{"Key": x['Key'], "Size": x['Size']} for x in resp['Contents']]

    ###################################################
    # 1) Get all objects/files in S3 bucket/folder
    # 2) Extract Key(Filename) and File Size
    ###################################################
    objects_list = []
    #resp = s3.list_objects(Bucket=BUCKET, Prefix=folder)
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=folder)
    objects_list.extend(resp_to_filelist(resp))

    # Get Next "page" of data
    while resp['IsTruncated']:
        # if there are more entries than can be returned in one request, the key
        # of the last entry returned acts as a pagination value for the next request
        logging.warning("Found {} objects so far".format(len(objects_list)))
        last_key = objects_list[-1][0]
        resp = s3.list_objects(Bucket=BUCKET, Prefix=folder, Marker=last_key)
        objects_list.extend(resp_to_filelist(resp))

    return objects_list


if __name__ == "__main__":

    try:   
        """ 
        parser = argparse.ArgumentParser(description="S3 file combiner")
        parser.add_argument("--bucket", help="base bucket to use")
        parser.add_argument("--folder", help="S3 folder whose contents should be combined")
        parser.add_argument("--prefix", help="prefix of files to combine into single file")
        parser.add_argument("--output", help="output location for resulting merged files, relative to the specified base bucket")
        parser.add_argument("--filesize", type=int, help="max filesize of the concatenated files in bytes")

        args = parser.parse_args()
        """

        #######################################################
        # Example parameters.
        #######################################################
        #args.bucket = 'aws-hhs-cms-eadg-bia-ddom-extracts-nonrpod'
        #args.folder = 'xtr/DEV/'
        #args.output = 'xtr/DEV/blbtn_clm_ext_20220812.091145.csv.gz'
        #args.prefix = 'blbtn_clm_ext_20220812.091145'
        #args.filesize = 1000000000

        ###############################################
        # Set global variable BUCKET with bucket name
        ###############################################
        global BUCKET
        BUCKET = "aws-hhs-cms-eadg-bia-ddom-extracts"
        #BUCKET = args.bucket
        #folder_to_concatenate =  args.folder
        #file_prefix = args.prefix
        #max_filesize = args.filesize
        folder = "xtr/OFM_PDE/"
        folder = "xtr/DOJ/"
        run_token = "20240805.153143"  # OFM
        run_token = "20240826.135600"  # DOJ

        # 40GB 32212254720-30GB  42949672960-40GB  53687091200-50GB
        iMaxSizeFiles = 42949672960  

        iMaxNOFFiles = 35
        iTotFileSize = 0
        iTotNOFFiles = 0

        iNOFBytes = 0

        Files2IncludeInManifest = []

        ######################################################
        # Get access to S3
        ######################################################
        s3 = new_s3_client()

        ######################################################
        # Get list of all files in S3 bucket/folder
        ######################################################
        s3FolderFileList = _list_all_objects_with_size(s3, folder)
        #print(s3FolderFileList)

        ######################################################
        # Filter list of files by run-token
        # 1) Tuple version  2) Dict version
        ######################################################
        #s3FolderFileListFiltered = [S3FldFilename for S3FldFilename in s3FolderFileList if S3FldFilename[0].find(run_token) != -1 ]
        Files2IncludeInManifest = [S3FilenameDict for S3FilenameDict in s3FolderFileList if str(S3FilenameDict['Key']).find(run_token) != -1 ]
        #print (Files2IncludeInManifest)

        ######################################################
        # Create Group Lists to ensure:
        #    1) Total NOF files not exceeded
        #    2) Total size of files in Manifest file is < 50 GB 
        ######################################################
        grouped_list = []
        current_list = []

        for File2Include in Files2IncludeInManifest:

            if (  ((iTotNOFFiles + 1)  > iMaxNOFFiles) or 
                
                  ((iTotFileSize + File2Include['Size']) > iMaxSizeFiles) ):
                print(f"{(iTotNOFFiles + 1)=}")
                print(f"{(iMaxNOFFiles)=}")
                print(f"{(iTotFileSize + File2Include['Size'])=}")
                print(f"{iMaxSizeFiles=}")

                print ("\nNew Group")

                grouped_list.append(current_list)
                current_list = []

                iTotNOFFiles = 0
                iTotFileSize = 0

                iNOFBytes = 0

            # end if


            # Add to current_list
            current_list.append(File2Include)

            iTotNOFFiles += 1
            iTotFileSize +=  File2Include['Size']

            print(f'{iTotFileSize=}')
            print(f"{File2Include['Size']=}")

            iNOFBytes += len(File2Include['Key']) + len(folder) + 70
            print(f'{iNOFBytes=}')

        ##################################################
        # Add remainder to group
        ##################################################
        if len(current_list) > 0:
            grouped_list.append(current_list)    


        ##################################################
        # Create a manifest file for each group
        ##################################################
        for group in grouped_list:
            print ("\n")
            print (f"{len(group)=}")
            print(group)
            # create manifest file; manifest filename add "-{group_#}" before "".json"
            #   


    except Exception as e:
        logging.error("Exception occured in CreateManifestFiles.py.")
        print(e)

        sys.exit(12)      