#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('Trust_evidence.db')
print("Open DB")
conn.execute('''CREATE TABLE Trust_evidence  
       (Delegation_id INTEGER PRIMARY KEY AUTOINCREMENT,
       Trustor_ip text,
       Trustee_ip text,
       Evidence_name INTEGER,
       Evidence_value INTEGER,     
       timestamp INTEGER DEFAULT CURRENT_TIMESTAMP) 
       ;''')
print("Done")
conn.close() 
