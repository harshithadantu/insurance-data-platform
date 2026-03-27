import sqlite3

conn=sqlite3.connect("data/source/sample.db")
cursor=conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS claims 
                (Policy_Id INTEGER,
                customer_id INTEGER,
               Claim_amount REAL,
               status TEXT)
               ''')

conn.commit()
conn.close()