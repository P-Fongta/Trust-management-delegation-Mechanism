from datetime import datetime
import json
import sqlite3
import asyncio
import aiocoap.resource as resource
from aiocoap import *
import aiocoap
import time
from E_collector import *
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from Delegate_All_Roles import Delegate_All_Roles
from Delegate_Trust_Computer_Repositor import Delegate_Trust_Computer_Repositor
from Delegate_Trust_Repositor import Delegate_Trust_Repositor
from Delegate_Evidence_Collector import Delegate_Evidence_Collector
from Delegate_Trust_Computer import Delegate_Trust_Computer, Trust_Computer
from Evidence_Storage import Evidence_Storage
from Trust_Value_Storage import Trust_Value_Storage
from Trust_Result import Trust_Result
from Trust_Evidence import Trust_Evidence
from Trust_Value import Trust_Value

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

class Handover_Request(resource.Resource):
    def __init__(self):
        super().__init__()

    async def Handover(self, old_delegate_IP, delegator_IP):
        print("\nStarting Handover...")
        x = {}
        for info in ["delegator_IP"]:
            x[info] = eval(info)
        y = json.dumps(x)
        payload = y.encode('ascii')
        print("\nSending: Delegation_Info_Request to [...%s]"%(str(old_delegate_IP.split(':', 4)[4])))
        protocol = await Context.create_client_context()
        request = Message(code=GET, payload=payload, uri=f'coap://[{old_delegate_IP}]/Delegation_Info_Request')
        #print('Payload: %s'%(payload))
        response = await protocol.request(request).response
        print('Recv: Delegation Information from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))
        response_data = json.loads(response.payload)
        Delegation_roles = response_data[0]['role']

        if 'TC' in Delegation_roles and 'TR' in Delegation_roles and 'EC' in Delegation_roles and 'DM' in Delegation_roles:
            #Store delegation info and run Delegation
            handler = Delegate_All_Roles()
            for item in response_data:
                handler.Delegate_all_roles_info(item) 
            print("\nStarting performing trust management on behalf of the delegators...")
            tasks = []
            for item in response_data:
                asyncio.create_task(handler.Delegate_all_roles(item)) 

        elif 'TC' in Delegation_roles and 'TR' in Delegation_roles:
            #Store delegation info and run Delegation
            handler = Delegate_Trust_Computer_Repositor()
            for item in response_data:
                handler.Delegate_Trust_Computer_Repositor_info(item) 
            print("\nStarting performing trust management on behalf of the delegators...")
            tasks = []
            for item in response_data:
                asyncio.create_task(handler.Delegate_Trust_Computer_Repositor(item)) 
        elif 'EC' in Delegation_roles:
            #Store delegation info and run Delegation
            handler = Delegate_Evidence_Collector()
            for item in response_data:
                handler.Delegate_Evidence_Collector_info(item) 
            print("\nStarting performing trust management on behalf of the delegators...")
            tasks = []
            for item in response_data:
                asyncio.create_task(handler.Delegate_Evidence_Collector_roles(item)) 
        elif 'TR' in Delegation_roles:
            #Store delegation info and run Delegation
            handler = Delegate_Trust_Repositor()
            for item in response_data:
                handler.Delegate_Trust_Repositor_info(item) 
            print("\nStarting performing trust management on behalf of the delegators...")
        elif 'TC' in Delegation_roles:
            #Store delegation info and run Delegation
            handler = Delegate_Trust_Computer()
            for item in response_data:
                handler.Delegate_Trust_Computer_info(item) 
            print("\nStarting performing trust management on behalf of the delegators...")
        
        #print("\n[Delegation] Sending Delegation Result to [...%s] DONE "%(str(trustor.split(':', 4)[4])))
    

    async def render_post(self, request):
        print("\nRecv: Handover_Request from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        data = json.loads(request.payload)
        old_delegate_IP =  data["delegate_IP"]
        delegator_IP =  data["delegator_IP"]

        # check if delegator’s delegation info already exists
        conn = sqlite3.connect(DB_Delegation)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM Delegation_info WHERE trustor_ip = ?",(delegator_IP,))
        exists = cur.fetchone() is not None
        conn.close()

        if exists:
            # nothing to do; return 2.04 Changed
            print("\nHandover skipped: delegation already exists")
            print("\nResp: to [...%s]" % (str(request.unresolved_remote.split(':', 4)[4])))
            payload = "Delegation already exists".encode('ascii')
            return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)
        else:
            await self.Handover(old_delegate_IP, delegator_IP)
            print("\nHandover Completed...")
            print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
            return aiocoap.Message(code=aiocoap.CREATED)
    
class Delegation_Info_Request(resource.Resource):
    def __init__(self):
        super().__init__()

    async def Info_Request(self, delegator_IP):
        #Retrive delegation information
        conn = sqlite3.connect(DB_Delegation)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = f"select * from Delegation_info where trustor_ip = ?"
        cur.execute(sql, (delegator_IP,))
        new_entries = cur.fetchall()
        conn.commit()
        all_trustee = []
        for row in new_entries: 
            x={}
            trustor = row["Trustor_ip"]
            trustee =  row["Trustee_ip"]
            lease_time =  row["Lease_time"]
            share =  row["share"]
            t_model =  row["T_model"]
            evidence = row["T_evidence"]
            t_update = row["T_update"]

            Roles =  row["Roles"]
            sql2 = "select * from Roles where Role_id = ? "
            cur.execute(sql2,(Roles,))
            row = cur.fetchone()
            if row: 
                role_str = row["role"]
                
            # convert unix time stamp to number of second from now
            now = datetime.now(tz=timezone.utc).timestamp()
            lease_time = lease_time - now 
            # convert some data to list
            evidence = [p.strip() for p in evidence.split(',') if p.strip()] 
            role = [p.strip() for p in role_str.split(',') if p.strip()]

            for info in ["trustor", "trustee", "lease_time","share","t_model","t_update","evidence","share","role"]:
                x[info] = eval(info)
            all_trustee.append(x)
        return all_trustee

        #print("\n[Delegation] Sending Delegation Result to [...%s] DONE "%(str(trustor.split(':', 4)[4])))
    

    async def render_get(self, request):
        print("\nRecv: Delegation_Info_Request from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        data = json.loads(request.payload)
        delegator_IP =  data["delegator_IP"]
        all_trustee = await self.Info_Request(delegator_IP)
        payload = json.dumps(all_trustee)
        payload = payload.encode('ascii')
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 

        return aiocoap.Message(payload=payload)
