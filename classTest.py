import datetime
import logging
import sys
import os


class geoCodeEventMetric(object):

    spacer = "  "   # class-level variable used by all instances

    def __init__(self, infile="", infile_cnt=0, infile_skip_rec_cnt=0, infile_clean="", infile_clean_cnt=0, outfile="", outfile_cnt = 0, start_time=None, end_time=None):
        self.infile = infile
        self.infile_cnt = infile_cnt
        self.infile_skip_rec_cnt = infile_skip_rec_cnt
        self.infile_clean = infile_clean
        self.infile_clean_cnt = infile_clean_cnt
        self.outfile = outfile
        self.outfile_cnt = outfile_cnt
        self.start_time = start_time
        self.end_time = end_time

    def elapsedTime(self):
        return self.end_time - self.start_time 

    def countDiff(self):
        diff =  self.infile_cnt - self.outfile_cnt
        return diff
        #return (date(self.infile_cnt - self.outfile_cnt)).strftime("%H:%M:%S")   

    def displayReportRec(self):
        rec = self.infile.ljust(15," ") 
        rec = rec + self.spacer
        rec = rec + str(self.infile_cnt).rjust(8," ")
        rec = rec + self.spacer
        rec = rec + self.infile_clean.ljust(20," ")
        rec = rec + self.spacer
        #rec = rec + str(self.infile_clean_cnt).rjust(8," ") 
        rec = rec + "{:,}".format(self.infile_clean_cnt).rjust(10," ") 
        rec = rec + self.spacer
        rec = rec + self.outfile.ljust(20," ")
        rec = rec + self.spacer
        rec = rec + str(self.outfile_cnt).rjust(8," ") 
        rec = rec + self.spacer
        rec = rec + str(self.elapsedTime()).rjust(12," ")
        return rec

    def displayReportHdr(self):
        logger.info("I can reference the logger from this class")
        rec = "Input File".ljust(15," ") 
        rec = rec + self.spacer
        rec = rec + "NOF Recs".ljust(8," ")
        rec = rec + self.spacer
        rec = rec + "Clean Input File".ljust(20," ")
        rec = rec + self.spacer
        rec = rec + "NOF Recs".ljust(8," ") 
        rec = rec + self.spacer
        rec = rec + "Output File".ljust(20," ")
        rec = rec + self.spacer
        rec = rec + "NOF Recs".ljust(8," ") 
        rec = rec + self.spacer
        rec = rec + "Elapsed Time".ljust(12," ")
        return rec        

# set up log file
log_dir = os.path.join(os.getcwd(), "temp")
logfile = os.path.join(log_dir,"paulClassLogging.log")

logging.basicConfig(
    #format="%(asctime)s %(levelname)-8s %(threadName)s %(funcName)s %(message)s", #--> %(name)s give logger name
    format="%(asctime)s %(levelname)-8s %(funcName)-12s %(message)s",
    encoding='utf-8',
    datefmt="%Y-%m-%d %H:%M:%S", 
    #filename=logfile, 
    handlers=[
    logging.FileHandler(logfile),
    logging.StreamHandler(sys.stdout)],
    level=logging.INFO)

logger = logging.getLogger() 

logger.info("Creating Metrics collection")

metrics = []

logger.info("Creating 1st geoCodingEventMetric object")

metric = geoCodeEventMetric()
metric.infile = "infile1.csv"
metric.infile_cnt = 50000
metric.infile_clean = "infile1_clean.csv"
metric.infile_clean_cnt=47000
metric.outfile="outfile1.csv"
metric.outfile_cnt = 46000
#metric.start_time=date = datetime.datetime(2021, 8, 5, 15, 23, 15)
metric.start_time = datetime.datetime(2021, 8, 6, 9, 23, 15)
metric.end_time = datetime.datetime.now()
metrics.append(metric)

logger.info("Creating 2nd geoCodingEventMetric object")
metric = geoCodeEventMetric()
metric.infile = "infile2.csv"
metric.infile_cnt = 54000000
metric.infile_clean = "infile2_clean.csv"
metric.infile_clean_cnt=45000000
metric.outfile="outfile2.csv"
metric.outfile_cnt = 43000000
#metric.start_time=date = datetime.datetime(2021, 8, 5, 15, 23, 15)
metric.start_time=date = datetime.datetime(2021, 8, 6, 9, 23, 15)
metric.end_time=date = datetime.datetime.now()
metrics.append(metric)

print(len(metrics))
print(metric.displayReportHdr())

logger.info("Loop thru Metric events and print")
for event in metrics:
    print(event.displayReportRec())


# Left-justified
print("{:<20}".format(123456789))
# Right-justified
print("{:>20}".format(123456789))


##d1 = datetime.strptime(d1, "%Y-%m-%d")
##return abs((d2 - d1).days)...

#print("countDiff: "+str(metric.countDiff()))
#print(datetime.datetime(2021, 8, 5, 15, 23, 15))

#print(metric.infile)
#print(metric.infile_cnt)
#print(metric.start_time)
#print("elapsedTime: "+str(metric.elapsedTime()))

logger.info("End of program")
