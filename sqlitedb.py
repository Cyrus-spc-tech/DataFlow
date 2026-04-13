import sqlite3
name='a.db'
con = sqlite3.connect(f"{name}")

cur = con.cursor()
userquery='From . . . '
cur.execute(f"{userquery}")

con.commit()
con.close()


q1="Create table {tname} ({colstr});"
q2="Select * from {tname};"
q3="Describe {tname};"
q4="Show Tables;"

class DDB:

    def __init__(self):
        db=sqlite3.connect('eg.db')
        cur=db.cursor()
        cur.execute("CREATE DATABASE IF NOT EXIST sampler ")

    # def fetch(self,db,table):




    

