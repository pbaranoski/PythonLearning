import sys
import time
import os

def stringNLTest():

    msgText = "The weekly Blue Button extract has completed.\n\n\tThe following file(s) were created:\n\t ${S3Files}"
    emailBody = ""
    msgTextArr = msgText.split("\n")
    for msg in msgTextArr:
        emailBody += msg + "\n" 

    print(emailBody)
    emailMsg = f"""
    Dear Mickey Mouse:

    {emailBody}

    Sincerely,
    Paul
    """

    print(emailMsg)


stringNLTest()
sys.exit(0)

def testFunc():

    #########################
    #
    #########################
    MAX_RETRIES = 3

    for _ in range(MAX_RETRIES):
        if os.path.exists("sentinelFile.txt"):
            print("someone's using the function")
            # wait
            print("sleeping...zzzz")
            time.sleep(1)
        else:
            print("jailbreak!")
            break
    else:   
        print("timeout condition!") 
        sys.exit(0)

    with open("sentinelFile.txt", "w") as sentinelFile:
        sentinelFile.write("")


    print("play with gitHub")

testFunc()

sys.exit(0)

import pandas 

#create DataFrame
df = pandas.DataFrame({'points': [25, 12, 15, 14, 19],
                   'assists': [5, 7, 7, 9, 12],
                   'rebounds': [11, 8, 10, 6, 6]})

print (df)

#insert new column 'player' as first column
#player_vals = ['A', 'B', 'C', 'D', 'E']
player_vals2 = ['X', 'Y', 'Z', 'R']
#df.insert(loc=0, column='player', value=player_vals2)
#print (df)

df["mouse"] = pandas.Series(player_vals2)
print(df)


 
           