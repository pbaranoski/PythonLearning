from tkinter import *
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title("sqlite3 test - to infinity and beyond!")
root.geometry("400x800")

# Databases

conn = sqlite3.connect("ToInfinityAndBeyond.db")
cur = conn.cursor()

cur.execute("""CREATE table Infinity
    (rocket text,
    engine_type text,
    drink text,
    NOF_missions integer,
    space_saying text
    )


""")

conn.commit()
conn.close()


root.mainloop()




