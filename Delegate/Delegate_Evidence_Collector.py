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
from Check_Lease_Time import Check_Lease_Time

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"
class Delegate_Evidence_Collector(resource.Resource):
    def __init__(self):
        super().__init__()

    def Delegate_Evidence_Collector_info(self, data):
        trustor = data["trustor"]
        trustee = data["trustee"]
        roles = ["EC"]
        roles = ','.join(roles)
        Trust_repositor_IP = data["Trust_repositor_IP"] 
        lease_time = data["lease_time"]
        evidence= data["evidence"]

        #convert data to database format
        evidence  = ','.join(data["evidence"])# specify evidence to store
        Evidence_collect = ','.join(data["evidence"])# specify evidence to collect
        Evidence_store  = ','.join(data["evidence"])# specify evidence to store
        leasing_time = datetime.timestamp(datetime.now())+lease_time
        print("\nStoring...Delegation Information Trustor[...%s] and Trustee[...%s]  "%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

        conn = sqlite3.connect(DB_Delegation)
        cursor_obj = conn.cursor()
        
        cursor_obj.execute("INSERT INTO Roles (role) VALUES (?)",(roles,))
        Role_id = cursor_obj.lastrowid
        conn.commit()

        cursor_obj.execute("INSERT INTO E_collector (Evidence) VALUES (?)",(Evidence_collect,))
        Ecollector_id = cursor_obj.lastrowid
        conn.commit()

        conn.execute("INSERT INTO Delegation_info (trustor_ip, trustee_ip, Roles, lease_time, E_collector, t_evidence) VALUES (?,?,?,?,?,?)",(trustor, trustee, Role_id, leasing_time, Ecollector_id, evidence))
        conn.commit()
        conn.close()
        conn1 = sqlite3.connect(DB_Trust_value) # assign trust value =0.5
        conn1.execute("INSERT INTO trust_value (trustor_ip, trustee_ip,trust_value) VALUES (?,?,?)",(trustor, trustee,"0.5"))
        conn1.commit()
        conn1.close() 

        print("\nStoring...Information Completed Trustor[...%s] and Trustee [...%s]"%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))
        
        #print("\n[Delegation] Sending Delegation Result to [...%s] DONE "%(str(trustor.split(':', 4)[4])))
    
    async def Send_evidence_to(self, data, sending_time):
        delegator_IP = data["trustor"]
        trustor = data["trustor"]
        trustee = data["trustee"]
        all_evidence = data["evidence"]
        Evidence_list=[]
        E_dict = {}
        for info in ["trustor", "trustee"]:
            E_dict[info] = eval(info)
        conn = sqlite3.connect(DB_Trust_evidence)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print(all_evidence)
        for p in all_evidence:
            if sending_time == "Period Send": #  Period Send or Immediate Send
                sql = f"select Evidence_id, Evidence_value from Trust_evidence where Evidence_name = ? and trustor_ip = ? and trustee_ip = ? ORDER BY timestamp"
                cur.execute(sql, (p,trustor,trustee))
                new_entries = cur.fetchall()
                conn.commit()
                for row in new_entries:
                    rowid = row[0]
                    evidence_value = row[1]
                    Evidence_list.append(evidence_value)
                    #print(Evidence_list)
                    sql2 = "DELETE FROM Trust_evidence WHERE Evidence_id = ?"
                    cur.execute(sql2, (rowid,))
                    conn.commit()
                E_dict[p]=Evidence_list.copy()
                Evidence_list=[]
            elif sending_time == "Immediate Send": #  Period Send or Immediate Send
                sql = f"select Evidence_id, Evidence_value from Trust_evidence where Evidence_name = ? and trustor_ip = ? and trustee_ip = ? ORDER BY timestamp DESC LIMIT 1"
                cur.execute(sql, (p,trustor,trustee))
                new_entries = cur.fetchall()
                conn.commit()
                for row in new_entries:
                    rowid = row[0]
                    evidence_value = row[1]
                    Evidence_list.append(evidence_value)
                    #print(Evidence_list)
                    sql2 = "DELETE FROM Trust_evidence WHERE Evidence_id = ?"
                    cur.execute(sql2, (rowid,))
                    conn.commit()
                E_dict[p]=Evidence_list.copy()
                Evidence_list=[]
        conn.close()
        y = json.dumps(E_dict)
        payload = y.encode('ascii')
        print("\nSending: Evidence_Storage to [...%s]"%(str(delegator_IP.split(':', 4)[4])))

        protocol = await Context.create_client_context()
        request = Message(code=POST, payload=payload, uri=f'coap://[{delegator_IP}]/Evidence_Storage')
        #print('Payload: %s'%(payload))
        response = await protocol.request(request).response
        print('Recv: from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))


    async def Delegate_Evidence_Collector_roles(self,data):
        # Define when a delegate returns the evidence to a delegator 
        sending_time = "Immediate Send" #  Period Send or Immediate Send

        trustor = data["trustor"]
        trustee = data["trustee"]
        IP = trustor,trustee
        conn = sqlite3.connect(DB_Delegation)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "select * from Delegation_info where trustor_ip = ? AND trustee_ip = ?"
        cur.execute(sql, (trustor, trustee))
        row = cur.fetchone()
        if row: 
            Ecollector_id = row["E_collector"]

        sql = "select * from E_collector where Ecollector_id = ? "
        cur.execute(sql, (Ecollector_id, ))
        row = cur.fetchone()
        if row: 
            evidence = row["Evidence"]
            evidence_list = [item.strip() for item in evidence.split(",")]

        if not row:
            print(f"No evidence collector info found for ID {Ecollector_id}")
        evidence_functions = {
        "distance": distance,
        "packet_loss_rate": packet_loss_rateF,
        "response_time": response_time,
        "availability": availability,
        "task_completion_rate": task_completion_rate
        }

         # if Period Send
        if sending_time == "Period Send":
            measurement_count = 1
            # Define frequency intervals
            Evidence_Collection_FREQ = 3600 # Every 1h
            Send_Evidence_FREQ = 3600 # Every 1h
            while True:
                tasks = []
                for evidence_item in evidence_list:
                    evidence_function = evidence_functions[evidence_item]
                    tasks.append(asyncio.create_task(evidence_function(IP)))
                await asyncio.wait(tasks)
                print('\n[Evidence Collection] Completed - Next update in 1 hour - Trustor[...%s] and Trustee[...%s]'%(str(trustor.split(':', 4)[4]), str(trustee.split(':', 4)[4])))
                
                if measurement_count % 5 == 0:
                    await self.Send_evidence_to(data, "Period Send")

                # Check lease time
                expiry = check_lease_time(trustor, trustee)
                if expiry:
                    print(f'\n[Evidence Collection] Delegation expired')
                    break
                
                measurement_count += 1
                # Reset counter to prevent overflow (optional)
                if measurement_count >= 36000:  # Reset after 10 hours
                    measurement_count = 0
                # Sleep for 1 m
                await asyncio.sleep(1) # 5s in simulation

        elif sending_time == "Immediate Send":
            i=0 
            while True:
                tasks = []
                for evidence_item in evidence_list:
                    evidence_function = evidence_functions[evidence_item]
                    tasks.append(asyncio.create_task(evidence_function(IP)))
                await asyncio.wait(tasks)
                print('\n[Evidence Collection] Completed - Trustor[...%s] and Trustee[...%s]'%(str(trustor.split(':', 4)[4]), str(trustee.split(':', 4)[4])))
                
                await self.Send_evidence_to(data, "Immediate Send")
                # Check lease time
                expiry = check_lease_time(trustor, trustee)
                # in experiments, we run just only 10 times instead of until lease time expires
                """ 
                if expiry:
                    print(f'\n[Evidence Collection] Delegation expired')
                    break
                """ 
                i=i+1
                time.sleep(1)
                

        

    async def render_post(self, request):
        data = json.loads(request.payload)
        print("\nRecv: Delegate_Evidence_Collector from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        #Store delegation info
        for item in data:
            self.Delegate_Evidence_Collector_info(item) 
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        print("\nStarting performing Evidence Collector on behalf of the delegators...")
        
        tasks = []
        for item in data:
            asyncio.create_task(self.Delegate_Evidence_Collector_roles(item)) 
        
        return aiocoap.Message(code=aiocoap.CREATED)

