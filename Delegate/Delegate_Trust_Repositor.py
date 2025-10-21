#!/usr/bin/env python3
from datetime import datetime
import threading
import multiprocessing
import logging
import json
import sqlite3
import asyncio
import uuid
import string
import statistics
import aiocoap.resource as resource
import aiocoap
from aiocoap import *
import subprocess
import time
from E_collector import *
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"
class Delegate_Trust_Repositor(resource.Resource):
    def __init__(self):
        super().__init__()

    def Delegate_Trust_Repositor_info(self, data):
        trustor = data["trustor"]
        trustee = data["trustee"]
        roles = ["TR"]
        roles = ','.join(roles)
        Trust_computer_IP = data["Trust_computer_IP"] 
        lease_time = data["lease_time"]
        evidence= data["evidence"]
        share = data["share"]

        #convert data to database format
        evidence  = ','.join(data["evidence"])
        Evidence_store  = ','.join(data["evidence"])# specify evidence to store
        leasing_time = datetime.timestamp(datetime.now())+lease_time
        print("\nStoring...Delegation Information Trustor[...%s] and Trustee[...%s]  "%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

        conn = sqlite3.connect(DB_Delegation)
        cursor_obj = conn.cursor()
        
        cursor_obj.execute("INSERT INTO Roles (role) VALUES (?)",(roles,))
        Role_id = cursor_obj.lastrowid
        conn.commit()

        cursor_obj.execute("INSERT INTO E_storage (Evidence) VALUES (?)",(Evidence_store,))
        Estorage_id = cursor_obj.lastrowid
        conn.commit()

        conn.execute("INSERT INTO Delegation_info (trustor_ip, trustee_ip, Roles, lease_time, E_storage, t_evidence, share) VALUES (?,?,?,?,?,?,?)",(trustor, trustee, Role_id, leasing_time, Estorage_id, evidence, share))
        conn.commit()
        conn.close()
        conn1 = sqlite3.connect(DB_Trust_value) # assign trust value =0.5
        conn1.execute("INSERT INTO trust_value (trustor_ip, trustee_ip,trust_value) VALUES (?,?,?)",(trustor, trustee,"0.5"))
        conn1.commit()
        conn1.close() 

        print("\nStoring...Information Completed Trustor[...%s] and Trustee [...%s]"%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))
        
        #print("\n[Delegation] Sending Delegation Result to [...%s] DONE "%(str(trustor.split(':', 4)[4])))
    

    async def render_post(self, request):
        data = json.loads(request.payload)
        print("\nRecv: Delegate_Evidence_Collector from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        #Store delegation info
        for item in data:
            self.Delegate_Trust_Repositor_info(item) 
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        print("\nStarting performing Evidence Storage on behalf of the delegators [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        return aiocoap.Message(code=aiocoap.CREATED)