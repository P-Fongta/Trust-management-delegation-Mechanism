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


async def Get_evidence_from(protocol, delegate_IP, data):
    trustor = data["trustor"]
    trustee = data["trustee"]
    all_evidence = data["evidence"]
    E_dict = {}
    for info in ["trustor", "trustee", "all_evidence"]:
        E_dict[info] = eval(info)
    y = json.dumps(E_dict)
    payload = y.encode('ascii')
    print("\nSending: Trust_Evidence to [...%s]"%(str(delegate_IP.split(':', 4)[4])))

    request = Message(code=GET, payload=payload, uri=f'coap://[{delegate_IP}]/Trust_Evidence')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))
    response_data = json.loads(response.payload)
    # Store the received evidence in database
    print('\nStoring Trust Evidence in Database')
    trustor = response_data["trustor"]
    trustee = response_data["trustee"]

    conn = sqlite3.connect(DB_Trust_evidence)
    for key_name, key_value in response_data.items():
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