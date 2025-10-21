#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('Delegation.db')
print("Open DB")
conn.execute('''CREATE TABLE Delegation_info  
       (Delegation_id INTEGER PRIMARY KEY AUTOINCREMENT,
       Trustor_ip text,
       Trustee_ip text,
       Roles INTEGER     ,
       Lease_time INTEGER,     
       T_model text,
       T_update text,
       E_storage INTEGER,
       E_collector INTEGER,
       d_making text,
       timestamp INTEGER DEFAULT CURRENT_TIMESTAMP) 
       ;''')
conn.execute('''CREATE TABLE E_storage  
       (Estorage_id INTEGER ,
       Evidence         TEXT)    
       ;''')
conn.execute('''CREATE TABLE E_collector 
       (Ecollector_id INTEGER ,
       Evidence         TEXT)    
       ;''')
conn.execute('''CREATE TABLE Roles
       (Role_id  INTEGER ,
       role    TEXT)    
       ;''')  
print("Done")
conn.close() 
