from tkinter import *
from PIL import ImageTk, Image
import sqlite3

global qryResults
global recNo
recNo = -1
global totRecs


def delete():
    
    conn = sqlite3.connect("ToInfinityAndBeyond.db")
    cur = conn.cursor()

    print(rocketKey)

    cur.execute (f"""
        DELETE FROM INFINITY
        where rocket = '{rocketKey}'   
        """
    )    

    conn.commit()
    conn.close()


def query():

    conn = sqlite3.connect("ToInfinityAndBeyond.db")
    cur = conn.cursor()

    cur.execute ("""
        SELECT  rocket, engine_type, drink, NOF_missions, space_saying, oid 
        FROM INFINITY  
        """
    )    


    #print("Here we sit!")
    records = cur.fetchall() 
    global totRecs 
    totRecs = len(records)
    global recNo
    recNo += 1

    print(f"recNo:{recNo}")
    #print(records) 

    global qryResults
    qryResults = ""

    for idx, rec in enumerate(records):
        print (rec)
        print(idx)

        if idx != recNo:
            continue

        if idx > recNo:
            break

        #if rec[0] == "":
        #    continue
        #else:
        #    qryResults = ""

        global rocketKey
        rocketKey = rec[0]

        for fld in rec:
        #    print(fld)
            qryResults += (str(fld) + "\n") 

 
    lblQueryResults.config(text=qryResults)


    conn.commit()
    conn.close()



def submit():

    conn = sqlite3.connect("ToInfinityAndBeyond.db")
    cur = conn.cursor()

    cur.execute ("""
        Insert into Infinity (rocket, engine_type, drink, NOF_missions, space_saying )           
        Values(:rocket, :engine_type, :InfinityDrink, :NOF_missions, :space_saying)
        """, 
        {
            'rocket' : rocket.get()
            ,'engine_type' : engine_type.get()
            ,'InfinityDrink' : InfinityDrink.get()
            ,'NOF_missions' : NOF_missions.get()
            ,'space_saying' : space_saying.get()
        }
    
    )

    conn.commit()
    conn.close()

    rocket.delete(0, END)
    engine_type.delete(0, END)
    InfinityDrink.delete(0,END)
    NOF_missions.delete(0,END)
    space_saying.delete(0,END)




root = Tk()
root.title("sqlite3 test - to infinity and beyond!")
root.geometry("400x300")

# Databases


'''
cur.execute("""CREATE table Infinity
    (rocket text,
    engine_type text,
    drink text,
    NOF_missions integer,
    space_saying text
    )
'''

lblRocket = Label(text="Rocket:")
lblRocket.grid(row=0, column=0, padx=20, sticky='e')
rocket = Entry(root, width=30)
rocket.grid(row=0, column=1, pady=5)

lblEngineType = Label(text="Engine Type:")
lblEngineType.grid(row=1, column=0, padx=20, sticky='e')
engine_type = Entry(root, width=30)
engine_type.grid(row=1, column=1)

lblDrink = Label(text="Space Drink:")
lblDrink.grid(row=2, column=0, padx=20, sticky='e')
InfinityDrink = Entry(root, width=30)
InfinityDrink.grid(row=2, column=1)

lblNOF_missions = Label(text="NOF Missions:")
lblNOF_missions.grid(row=3, column=0, padx=20, sticky='e')
NOF_missions = Entry(root, width=30)
NOF_missions.grid(row=3, column=1)

lblSpace_saying = Label(text="Space Saying:")
lblSpace_saying.grid(row=4, column=0, padx=20, sticky='e')
space_saying = Entry(root, width=30)
space_saying.grid(row=4, column=1)

submitBtn = Button(root, text="Submit", command=submit)
submitBtn.grid(row=5, column=1, padx=10, pady=5, ipadx=50)

submitBtn = Button(root, text="Query", command=query)
submitBtn.grid(row=6, column=1, padx=10, pady=5, ipadx=50)

deleteBtn = Button(root, text="Delete", command=delete)
deleteBtn.grid(row=7, column=1, padx=10, pady=5, ipadx=50)

lblQueryResults = Label(text="")
lblQueryResults.grid(row=9, column=1, padx=10, pady=5)

root.mainloop()




