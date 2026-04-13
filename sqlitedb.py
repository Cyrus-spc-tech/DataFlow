import sqlite3
name='a.db'
con = sqlite3.connect(f"{name}")

cur = con.cursor()
userquery='From . . . '
cur.execute(f"{userquery}")

con.commit()
con.close()

