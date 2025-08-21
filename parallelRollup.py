from datetime import datetime
import combineS3Files as combiner
from multiprocessing import Pool

def folders_at_level(base_folder, level):
    # This function returns all of the S3 folders at a given depth level
    # underneath the base folder.
    # This allows a list to be built up of folders that should have their
    # contents concatenated.
    # Example:   level --> 1 2 3
    #                      | | |
    #          base_folder/a/b/c
    s3 = combiner.new_s3_client()
    return {'/'.join(k[0].split('/')[:level+1]) for k in combiner.collect_parts(s3, base_folder, "")}

def rollup(input_folder):
    # parallel map function only takes 1 arg
    combiner.run_concatenation(input_folder, "pythonrollup/{}/all.json".format(input_folder), "")

if __name__ == '__main__':
    print("Start: {}".format(datetime.now()))
    folders_to_rollup = folders_at_level("split-2015-07-06", 3)
    print("Folders: {}".format(folders_to_rollup))
    print("Finished Getting S3 Listing: {}".format(datetime.now()))
    pool = Pool(processes=128)
    pool.map(rollup, folders_to_rollup, 200)
    print("End: {}".format(datetime.now()))