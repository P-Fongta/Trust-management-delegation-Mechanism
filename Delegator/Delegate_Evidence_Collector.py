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

DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

async def Delegate_Evidence_Collector(protocol,delegate_IP, x):
    print("####################Delegation Evidence Collector Roles####################")
    print("Trustor IP: [%s]"%x[0]["trustor"])
    print("Delegate IP: [%s]"%delegate_IP)
    for node in x:
        trustee = node["trustee"]
        evidence = node["evidence"]
        lease_time = node["lease_time"]
        print("Trustee IP: [%s]"%trustee)
        print("Evidence : [%s]"%evidence)
    print("###################################################################")
    await asyncio.sleep(1)
    print('\nSending: Delegate_Evidence_Collector to [...%s]'%str(delegate_IP.split(':', 4)[4]))
    y = json.dumps(x)
    payload = y.encode('ascii')
    request = Message(code=POST, payload=payload, uri=f'coap://[{delegate_IP}]/Delegate_Evidence_Collector')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))