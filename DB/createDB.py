#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('Service_Registration.db')
print("Open DB")

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
conn.execute('''CREATE TABLE Trust_model
       (TModel_id  INTEGER ,
       Trust_model    TEXT)    
       ;''')
conn.execute('''CREATE TABLE Decision_making_method
       (DMaking_id  INTEGER ,
       Decision_making    TEXT)    
       ;''')
conn.execute('''CREATE TABLE Delegation_Registration
       (
       Reg_id  INTEGER PRIMARY KEY ,
       Delegate_ip          TEXT    ,
       Lease_time        INTEGER,
       Roles INTEGER,
       Trust_model INTEGER,
       E_storage INTEGER,
       E_collector INTEGER,
       D_maker INTEGER,
       timestamp INTEGER DEFAULT CURRENT_TIMESTAMP
       )
       ;''')
"""
INSERT INTO "Trust_model" ("TModel_id","Trust_model") VALUES (NULL,'weighted sum');

INSERT INTO "Trust_model" ("TModel_id","Trust_model") VALUES (NULL,'fuzzy-logic');

INSERT INTO "Decision_making_method" ("DMaking_id","Decision_making") VALUES (NULL,'TD');

INSERT INTO "Decision_making_method" ("DMaking_id","Decision_making") VALUES (NULL,'TBD');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'response time');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'availability');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'distance');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'cooperativeness');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'task completion rate');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'packet loss rate');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'reputability');

INSERT INTO "E_storage" ("Estorage_id","Evidence") VALUES (NULL,'network latency');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'response time');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'availability');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'distance');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'cooperativeness');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'task completion rate');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'packet loss rate');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'reputability');

INSERT INTO "E_collector" ("Ecollector_id","Evidence") VALUES (NULL,'network latency');

INSERT INTO "Roles" ("Role_id","role") VALUES (NULL,'TC');

INSERT INTO "Roles" ("Role_id","role") VALUES (NULL,'TR');

INSERT INTO "Roles" ("Role_id","role") VALUES (NULL,'EC');

INSERT INTO "Roles" ("Role_id","role") VALUES (NULL,'DM');
"""
print("Done")
conn.close() 
print("Done")
conn.close() 
