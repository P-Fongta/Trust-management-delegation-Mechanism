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
class Trust_Evidence(resource.Resource): # used for GET /Trust_Evidence
    def __init__(self):
        super().__init__()

    def Return_evidence(self,data):
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
        for p in all_evidence:
            sql = f"select Evidence_id, Evidence_value from Trust_evidence where Evidence_name = ? and trustor_ip = ? and trustee_ip = ? ORDER BY timestamp"
            cur.execute(sql, (p,trustor,trustee))
            new_entries = cur.fetchall()
            conn.commit()
            for row in new_entries:
                evidence_value = row[1]
                Evidence_list.append(evidence_value)
            E_dict[p]=Evidence_list.copy()
            Evidence_list=[]
            
        conn.close()
        evidence_result = E_dict
        return evidence_result

    async def render_get(self, request):
        print('\nRecv: Trust_Evidence from %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        data = json.loads(request.payload)
        #print(json.dumps(data))
        payload = self.Return_evidence(data)
        print('\nResp: to %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        payload = json.dumps(payload)
        payload = payload.encode('ascii')
        print('\nResp: to %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        #print("\nResp: to {}".format(request.unresolved_remote))
        return aiocoap.Message(payload=payload)