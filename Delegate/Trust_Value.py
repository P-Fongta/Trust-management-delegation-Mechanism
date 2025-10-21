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
class Trust_Value(resource.Resource): # used for GET /Trust_Value
    def __init__(self):
        super().__init__()

    def Get_trust_value(self,data):
        trustor_ip = data["trustor"]
        trustee_ip = data["trustee"]
        trust_value= {}

        conn = sqlite3.connect(DB_Trust_value)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "select * from Trust_value where trustor_ip = ? AND trustee_ip = ?"
        cur.execute(sql,(trustor_ip,trustee_ip))
        row = cur.fetchone()
        if row: 
            trust_value["trust_value"]= row["trust_value"]
        conn.close()


        return trust_value

    async def render_get(self, request):
        print("\nRecv: Trust_Value from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        data = json.loads(request.payload)
        payload = self.Get_trust_value(data)
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4])))  
        payload = json.dumps(payload)
        payload = payload.encode('ascii')
        #print("\nResp: to {}".format(request.unresolved_remote))
        return aiocoap.Message(payload=payload)