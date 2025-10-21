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

DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

class Evidence_Storage(resource.Resource):
    def __init__(self):
        super().__init__()


    async def E_storage(self,data):
        trustor = data["trustor"]
        trustee = data["trustee"]

        conn = sqlite3.connect(DB_Trust_evidence)
        for key_name, key_value in data.items():
            if key_name in ["trustor", "trustee"]:
                continue
            if isinstance(key_value, (list, tuple)):
                values = key_value
            else:
                values = [key_value]  # Convert single value to list

            for value in values:
                conn.execute(
                        "INSERT INTO Trust_evidence (trustor_ip, trustee_ip, Evidence_name, Evidence_value) VALUES (?,?,?,?)",
                        (trustor, trustee, key_name, value)
                    )
        conn.commit()
        conn.close()
        print('\n[EVIDENCE_STORAGE] Completed Trustor[...%s] and Trustee [...%s]'%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: EVIDENCE_STORAGE from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))
        await self.E_storage(data)  
        return aiocoap.Message(code=aiocoap.CREATED)