#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('Trust_value.db')
print("Open DB")
conn.execute('''CREATE TABLE Trust_value  
       (TValue_id INTEGER PRIMARY KEY AUTOINCREMENT,
       Trustor_ip text,
       Trustee_ip text,
       Trust_value REAL     ,
       timestamp INTEGER DEFAULT CURRENT_TIMESTAMP) 
       ;''')
 
print("Done")
conn.close() 
