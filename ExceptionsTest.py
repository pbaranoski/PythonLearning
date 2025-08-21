import traceback
import logging
import logging.config
import sys
import os
import datetime

# import external file with a function
import importTest

class RainyDayException(Exception):
    "Rainy Days and Mondays really stink!"


def fnc_divide(n):

    logger.info("in fnc_divide")

    try:
        result=n/0
        logger.info("The result=",result)

    #except Exception as e:  # this is fine but messages appeared to be root messages only. So, logger must be set-up correctly.
    except:
        # "display "ERROR:root:The exc_info - Zero Division error"
        # Taylor info message does not display
        logging.info("Taylor")
        logging.exception('The exc_info - Zero Division error')

def func1(s):

    try:
        #assert will throw an Exception if condition is not true
        #assert s == "Paul"

        logger.info("s: "+ s)
        logger.info("doing more stuff")
        logger.info("before exception")

        logger.info("test for displaying stack info. ",stack_info=True)

        #raise Exception ("General Exception occurred")
        raise RainyDayException()
        #raise ValueError('A very specific bad thing happened.')

        logger.info ("after exception")

    except:    
        #print (repr(error))  #repr converts object to string value
        #print(error.__cause__)  # None
        logger.exception("Exception caught in function")
        #print ("Exception caught in function \n"+traceback.format_exc())
        #print("re-raise exception to be caught by outer block")
        logger.error("logging some information Paul")
        raise
        #raise RuntimeError("chaining an error to existing error") from error
        #raise AssertionError("Unexpected value of 'distance'!")  # for errors that should not happen, code for assert


try:

    print (__name__) #--> this prints "__main__"

    # call function in external file
    importTest.workingDir()

    log_dir = os.getcwd()
    log_dir = os.path.join(log_dir, "temp")

    print(log_dir)

    logfile = os.path.join(log_dir,"paulLogging.log")
    print(logfile)

    #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 

    #****\/*****
    #--> for setting same log information to both screen and log file
    #--> Appears to be most accurate way to capture information
    """
    logging.basicConfig(
        #format="%(asctime)s %(levelname)-8s %(threadName)s %(name)s %(message)s", #--> %(name)s give logger name
        format="%(asctime)s %(levelname)-8s %(funcName)-12s %(message)s",
        encoding='utf-8',
        datefmt="%Y-%m-%d %H:%M:%S", 
        #filename=logfile, 
        handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout)],
        level=logging.INFO)
    """    
    #*****/\*****    
    
    logger = logging.getLogger()  # get root logger.  Too many errors using a named logger.  Messages at root are missed.
    print("logger: "+str(logging.getLogger()))

    #*****\/*****
    #--> for setting different log information to screen vs log file
    """
    logger.setLevel(logging.INFO)

    print_format = logging.Formatter('%(levelname)-8s %(funcName)-12s %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(print_format)

    # create a log file handler
    # and define a custom log format, set its log level to DEBUG
    log_format = logging.Formatter('[%(asctime)s] %(levelname)-8s %(funcName)-12s %(message)s')
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    """
    #*****/\*****

    #*****\/*****
    # --> file Config for logger
    # --> capture error in function fnc_divide to console, but NOT in log file.  Buggy
    logging.config.fileConfig("C:\\Users\\user\\Documents\\PythonLearning\\config\\loggerConfig.txt", disable_existing_loggers=False)
    #*****/\*****

    logger.info("\n########")
    logger.info("Program started")

    fnc_divide(6)

    func1("calling function")

    logger.info("after function call")

except:
    logger.exception("exception caught in main code: ")
    #logger.debug("testing debug option", stack_info: true)  
    #, stack_info, stacklevel and extra.




