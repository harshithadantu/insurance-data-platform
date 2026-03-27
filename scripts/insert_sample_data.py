import sqlite3
import random

conn=sqlite3.connect("data/source/sample.db")
cursor=conn.cursor()

for i in range(1000):
    policy_id=random.randint(1000,2000)
    customer_id=random.randint(5000,6000)
    claim_amount=random.uniform(100,5000)
    status=random.choice(['Approved','Rejected','Pending'])
    
    cursor.execute('''
                   INSERT INTO claims (Policy_Id, customer_id, Claim_amount, status)
                   VALUES (?, ?, ?, ?)
                   ''', (policy_id, customer_id, claim_amount, status))

conn.commit()
conn.close()