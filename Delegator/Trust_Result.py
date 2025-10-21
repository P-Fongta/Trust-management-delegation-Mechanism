#!/usr/bin/env python3


from datetime import datetime
import logging
import asyncio
import json
import subprocess
from aiocoap import *

async def Trust_Result(protocol,delegate_IP, node, decision_type, threshold):
    
    if decision_type == "TD":
        trustor = node["trustor"]
        trustee = node["trustee"]
        D = {}
        for info in ["trustor", "trustee", "threshold"]:
            D[info] = eval(info)
        y = json.dumps(D)
        payload = y.encode('ascii')
        print("\nSending: Trust_Result to [...%s]"%(str(delegate_IP.split(':', 4)[4])))
        request = Message(code=GET, payload=payload, uri=f'coap://[{delegate_IP}]/Trust_Result')
        #print('Payload: %s'%(payload))
        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch Trust:')
            print(e)
        else:
            trust_result = json.loads(response.payload)
        print("\nRecv: Trust of [...%s] = %r"%(str(trustee.split(':', 4)[4]), trust_result["trust"]))
        
    elif decision_type == "TBD":
        trustor = node[0]["trustor"]    
        trustee_list = [n["trustee"] for n in node]
        trust_info = {"trustor": trustor,"threshold": threshold, "trustee": trustee_list}
        y = json.dumps(trust_info)
        #print(y)
        payload = y.encode('ascii')
        print("\nSending: Trust_Result to [...%s]"%(str(delegate_IP.split(':', 4)[4])))
        request = Message(code=GET, payload=payload, uri=f'coap://[{delegate_IP}]/Trust_Result')
        #print('Payload: %s'%(payload))
        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch Trust:')
            print(e)
        else:
            trust_result = json.loads(response.payload)
            print("\nRecv: Highest Trustee IP [%s] Value %s"%(trust_result["highest_trustee"], trust_result["highest_value"]))
      