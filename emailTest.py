
import smtplib
import sys


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
        #smtpServer.send_message(sender,receivers, message)     
        print ("Successfully sent email")

        smtpServer.close()

    except smtplib.SMTPSenderRefused as ex:
        print ("SMTP Error: Sender Refused")
        print(ex.smtp_error)
        print(ex.sender)
        raise

    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Error: SMTP Authorization failed") 
        print(e.smtp_error)
        print(e.strerror)
        raise

    except smtplib.SMTPNotSupportedError as es:
        print("SMTP Error: Auth Extension not supported by server")
        print(es.strerror) 
        raise

    except smtplib.SMTPException as x:
        print("SMTP Error: Exception")
        print(x.with_traceback()) 
        raise        
        
        
#######################################################
# Is the module being called by a shell script?
#######################################################        
if len(sys.argv) > 0:
    # module being called
    lstParms = sys.argv
    sender = lstParms[1]
    receivers = lstParms[2]
    subject = lstParms[3]
    messageText = lstParms[4]
    print(f"sender:{sender}")
    print(f"receivers:{receivers}")
    print(f"subject:{subject}") 
    print(f"messageText:{messageText}")   
    try:    
        sendEmail(sender, receivers, subject, messageText)
    except: 
        sys.exit(12)
    
else:
    # module NOT called from shell script
    pass 
    
    

