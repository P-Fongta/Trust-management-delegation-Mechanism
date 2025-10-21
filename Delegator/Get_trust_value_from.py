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


async def Get_trust_value_from(protocol, delegate_IP, data):

    trustor = data["trustor"]
    trustee = data["trustee"]
    x = {}
    for info in ["trustor", "trustee"]:
            x[info] = eval(info)
    print('\nSending: Trust_value to [...%s]'%str(delegate_IP.split(':', 4)[4]))
    y = json.dumps(x)
    payload = y.encode('ascii')
    request = Message(code=GET, payload=payload, uri=f'coap://[{delegate_IP}]/Trust_value')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    data = json.loads(response.payload)
    trust_value = data["trust_value"]
    print('Recv: from [...%s] Trust Value: %s'%(str(response.unresolved_remote.split(':', 4)[4]), trust_value))
    