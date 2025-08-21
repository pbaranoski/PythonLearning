import datetime
import sys
import gzip
import json
import os
import re

#import datetime
from datetime import datetime
from datetime import date,timedelta

import logging

from io import StringIO


def create_logger(name, log_file, level=logging.INFO):
    """Set up a logger that writes logs to a specified file."""
    # Create a file handler that logs messages to the specified file
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    
    return logger

def main_processing():
    ## Setting up the first logger for the first log file
    first_logger = create_logger('Child', 'Child.log')
    first_logger.info('Logging to the child log file as an info message.')

if __name__ == "__main__":
    main_processing()





