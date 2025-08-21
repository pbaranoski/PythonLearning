
from email.mime.text import MIMEText
import smtplib
import os


def sendEmail(sender, receivers, subject, messageText):

    sToEmails = ""

    lstReceivers = receivers.split(",")
    sToEmails = "<" + ">,<".join(lstReceivers) + ">"


    message = f"""From: <{sender}>
To: {sToEmails}
Subject: {subject}

{messageText}

    """
        
    try:
        ###\/####
        # plain/html
        msg = MIMEText(messageText, 'html')
        msg['Subject']= subject   
        msg['From']   = sender
        ####/\####


        #print("Before getting smtpServer")	
        smtpServer = smtplib.SMTP('localhost', 25, None)
        print("SMTP: Connected to smtpServer")

        smtpServer.ehlo()
        print("SMTP ehlo: Successfully identified as client to server")
        #print("setdebuglevel")
        smtpServer.set_debuglevel(1)
        print("STMP: set debuglevel")
        smtpServer.ehlo()
        #print("after ehlo")

        smtpServer.sendmail(sender, receivers, message)  
        msg.as_string()       
        print ("Successfully sent email")

        smtpServer.close()

    except smtplib.SMTPSenderRefused as ex:
        print ("SMTP Error: Sender Refused")
        print(ex.smtp_error)
        print(ex.sender)

    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Error: SMTP Authorization failed") 
        print(e.smtp_error)
        print(e.strerror)

    except smtplib.SMTPNotSupportedError as es:
        print("SMTP Error: Auth Extension not supported by server")
        print(es.strerror)  

    except smtplib.SMTPException as x:
        print("SMTP Error: Exception")
        print(x.with_traceback())  

#sendEmail("pbaranoski@apprioinc.com", "pbaranoski@apprioinc.com, sgayam@apprioinc.com", "Subject matter", "Messages")

import datetime

now = datetime.datetime.now()
iMonth = int(now.strftime("%m"))
#var1 = sys.argv[1]

# Set Extract type
if iMonth < 3:
    EXT_TYPE = "M12"
elif iMonth >= 3 and iMonth <= 6:
    EXT_TYPE = "EARLYCUT"
else:
    EXT_TYPE = "FINAL"
