#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('Access_permission.db')
print("Open DB")
conn.execute('''CREATE TABLE Access_permission
   (P_id INTEGER PRIMARY KEY AUTOINCREMENT,
   IP_address TEXT,
   Permission TEXT,
   Trustor_IP TEXT)
   ;''')
 
print("Done")
conn.close() 
