#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('report.db')
print("Open DB")
cursor_obj = conn.cursor()
conn.execute('''CREATE TABLE broken_down_vehicles 
       (e_id INTEGER PRIMARY KEY AUTOINCREMENT,
       device_ip text     NOT NULL,
       msg text     NOT NULL,
       timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')))     
       ;''')

conn.commit()

conn.execute('''CREATE TABLE V_state  
       (e_id INTEGER PRIMARY KEY AUTOINCREMENT,
       device_ip text     NOT NULL,
       speed text     NOT NULL,
       location    REAL,
       dest    REAL,
       timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')))      
       ;''')
conn.commit()   

print("Done")
conn.close() 
