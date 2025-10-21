#!/usr/bin/env python3


from datetime import datetime
import logging
import asyncio
import json
import subprocess
from aiocoap import *
from E_collector import *

# logging setup
#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)

from Delegate_Trust_Computer import Delegate_Trust_Computer
from Trust_Computer import Trust_Computer
from Trust_Result import Trust_Result

async def Delegate_Trust_Computer(protocol,delegate_IP, x):
    print("####################Delegation Trust Computer Role####################")
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
    print('\nSending: Delegate_Trust_Computer to [...%s]'%str(delegate_IP.split(':', 4)[4]))
    y = json.dumps(x)
    payload = y.encode('ascii')
    request = Message(code=POST, payload=payload, uri=f'coap://[{delegate_IP}]/Delegate_Trust_Computer')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(delegate_IP.split(':', 4)[4]), response.code))