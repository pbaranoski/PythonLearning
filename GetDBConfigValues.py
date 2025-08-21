# Get DB configuration values

import os
import configparser

class ConfigFileNotfnd(Exception):
    "Configuration file not found: "

###############################
# Get DB config filename
###############################
curDir = os.getcwd()
configPath = os.path.join(curDir,"config")
configPathFilename = os.path.join(configPath,"DBConfig.txt")
if os.path.exists(configPathFilename):
    #print("File exists: "+configPathFilename)
    pass
else:
    raise ConfigFileNotfnd(configPathFilename)

###############################
# Extract configuration values
###############################
config = configparser.ConfigParser()
config.read(configPathFilename)
#print (config.sections())

DBUser = config.get('DBSect','DBUser')
DBPswd = config.get('DBSect','DBPswd')
DBHost = config.get('DBSect','host')
DBDatabase = config.get('DBSect','database')


