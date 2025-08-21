import json


dict_event = {

    "method": "POST",
    "deleteReason": "",
    "fileInformation": [
        {
            "fileName": "aws-hhs-cms-eadg-bia-ddom-extracts/xtr/Finder_Files/archive/DEMO_FINDER_PLNH0137_20230718_103000.txt",
            "fileLocation": "xtr/NYSPAP/"
        }
    ],
    "shareDetails": {
        "dataRequestID": "IDRBI-64943-20240201-130547",
        "shareDuration": "30",
        "dataRecipientEmails": "robert.palumbo@primetherapeutics.com,bit-extractalerts@index-analytics.com",
        "totalNumberOfFiles": "1",
        "jiraTicket": "https://jiraent.cms.gov/browse/IDRBI-64943"
    },
    "requestorContactInfo": {
        "fullName": "Karen Allen",
        "phoneNumber": "443-602-6853",
        "email": "karen.allen@cms.hhs.gov"
    },
    "comments": ""
}

dict_event2 = {

    "method": "POST",
    "deleteReason": "",
    "fileInformation": [
        {
            "fileName": "aws-hhs-cms-eadg-bia-ddom-extracts/xtr/Finder_Files/DEMO_FINDER_PLNH0137_20230718_103000.txt",
            "fileLocation": "xtr/NYSPAP/"
        }
    ],
    "shareDetails": {
        "dataRequestID": "IDRBI-64943-20240201-130547",
        "shareDuration": "30",
        "dataRecipientEmails": "robert.palumbo@primetherapeutics.com,bit-extractalerts@index-analytics.com",
        "totalNumberOfFiles": "1",
        "jiraTicket": "https://jiraent.cms.gov/browse/IDRBI-64943"
    },
    "requestorContactInfo": {
        "fullName": "Karen Allen",
        "phoneNumber": "443-602-6853",
        "email": "karen.allen@cms.hhs.gov"
    },
    "comments": ""
}

#############################################
# ignore event
#############################################
lFileInfo=dict_event.get('fileInformation')
print(lFileInfo)
fileName = lFileInfo[0].get('fileName')
print(fileName)

rsp=fileName.find('Finder_Files/archive/')
if rsp != -1:
    print('ignore this event')
else:
    print('process this event')    

#############################################
# process event
#############################################
lFileInfo=dict_event2.get('fileInformation')
print(lFileInfo)
fileName = lFileInfo[0].get('fileName')
print(fileName)

rsp=fileName.find('Finder_Files/archive/')
if rsp != -1:
    print('ignore this event')
else:
    print('process this event')    