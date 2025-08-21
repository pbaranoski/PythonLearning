import os
import sys
import traceback

in_dir = r"C:\FamilyTreeMaker"
out_dir = r"C:\FamilyTreeMaker"

in_file = os.path.join(in_dir,"FamilyMember.txt")
out_file = os.path.join(in_dir,"FamilyMember.csv")

date_flds = [5,6,9,10]

################################
# functions
################################
def convertDt(dt):
    ###print("convertDt"+ dt)
    
    #dt in m/d/yyyy format
    mmddyyyy = dt.split("/")
    if (len(mmddyyyy) == 3):
        mm = ('0' + mmddyyyy[0])[-2:]
        dd = ('0' + mmddyyyy[1])[-2:]
        yyyy = mmddyyyy[2]
        return "{}-{}-{}".format(yyyy,mm,dd)
    elif dt == "":
        return "NULL"
    else:    
        return dt

    #return "%s-%s-%s" % (yyyy,mm,dd)


def isDateFld(idx):

    try:
        if date_flds.index(idx) >= 0:
            return True
    except:
        return False        


def isNumber(fld):

    testFld = fld
    return str(testFld).isnumeric()        

################################
# main
################################

#print (convertDt('9/4/1964'))
#print (convertDt('09/04/1964'))

# init ctr
rec_ctr = 0

# process file
with open(in_file,"r",encoding="utf-8") as iftxt, open(out_file,"w",encoding="utf-8") as ofcsv:

    inrecs = iftxt.readlines()

    for inrec in inrecs:
        #rec = inrec.decode("utf-8")
        rec = inrec
        # remove first character
        rec = rec[1:] 

        rec_ctr += 1

        # Skip first record
        if (rec_ctr == 1):
            continue

        # Skip filler lines    
        if (rec[0 : 5] == "-----"):
            continue

        # MySQL Workbench appears to hiccup on this value and stops importing records.  
        rec = rec.replace("Ł","L")  

        # split record by delimiter into separate fields  
        flds = rec.split("|")

        out_rec = ""
        nof = len(flds)

        # process fields in record
        for idx in range(len(flds)):

            # remove leading and trailing spaces
            fld = flds[idx].strip()

            # special processing for fields defined as dates
            if isDateFld(idx):
                fld = convertDt(fld)
            # if fld is not numeric, places contents in quotes
            #elif isNumber(fld):
            #    pass
            #else:
            #    fld = '"' + fld + '"'

            #!!!! Issue with Ł character.  Need to convert to L

            # if fld contains a comma, place contents in quotes
            if (fld.find(",") >= 0):
                fld = '"' + fld + '"'

            out_rec = out_rec + fld + ","


        # remove extra, ending delimiter
        out_rec = out_rec[:-2]
        #print (out_rec)

        ofcsv.write(out_rec + '\n')

        #if rec_ctr > 2:
        #    break



sys.exit(0)





      
