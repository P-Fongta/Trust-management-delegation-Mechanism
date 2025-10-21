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

# logging setup
#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"
DB_Access_Permission= "/home/pi/aiocoap/DB/Access_permission"
      

class Grant_Permission(resource.Resource): 
    def __init__(self):
        super().__init__()


    async def Grant_Permission(self,data):
        trustor_ip = Grant_Permission['trustor']
        for key, value in Grant_Permission.items():
            if key == 'trustor':
                continue
            p_address = value[0]
            permissions = value

        conn = sqlite3.connect(DB_Access_Permission)
        for permission in permissions:
            conn.execute(
                    "INSERT INTO Access_permission (IP_address, Permission, Trustor_IP) VALUES (?,?,?)",
                    (p_address, permission, trustor_ip)
                )
        conn.commit()
        conn.close()
        print('\n[Permission Grant] Completed Trustor[...%s] and Trustee [...%s]'%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: Grant_Permission from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))
        await self.Grant_Permission(data)  
        print('\nResp: to %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        return aiocoap.Message(code=aiocoap.CREATED)
    
class Revoke_Permission(resource.Resource):
    def __init__(self):
        super().__init__()


    async def Revoke_Permission(self,data):
        trustor_ip = Grant_Permission['trustor']

        conn = sqlite3.connect(DB_Access_Permission)
        conn.execute("DELETE FROM Access_permission where Trustor_IP = trustor_ip ")
        conn.commit()
        conn.close()
        print('\n[Permission Revocation] Completed Trustor[...%s] and Trustee [...%s]'%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: Revoke_Permission from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))
        await self.Revoke_Permission(data)  
        print('\nResp: to %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        return aiocoap.Message(code=aiocoap.DELETED)

