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
class Trust_Value_Storage(resource.Resource): #used for POST /Trust_Value_Storage
    def __init__(self):
        super().__init__()


    async def TV_storage(self,data):
        trustor = data["trustor"]
        trustee = data["trustee"]
        Trust_value = data["Trust_value"]

        conn = sqlite3.connect(DB_Trust_value)
        conn.execute(
                "INSERT INTO Trust_value (trustor_ip, trustee_ip, Trust_value) VALUES (?,?,?)",
                (trustor, trustee, Trust_value)
            )
        conn.commit()
        conn.close()
        print('\n[TRUST_VALUE_STORAGE] Completed Trustor[...%s] and Trustee [...%s]'%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: Trust_Value_Storage from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))
        await self.TV_storage(data)  
        print('\nResp: to %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        return aiocoap.Message(code=aiocoap.CREATED)
