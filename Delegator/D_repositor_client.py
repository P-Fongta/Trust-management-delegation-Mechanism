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

from Delegate_Trust_Repositor import Delegate_Trust_Repositor
from Send_evidence_to import Send_evidence_to
from Get_evidence_from import Get_evidence_from
from Get_trust_value_from import Get_trust_value_from


async def GetEvidence_UpdateTrust_SendTrust_to(protocol, delegator_IP, data):
    trustor = data["trustor"]
    trustee = data["trustee"]
    evidence = data["evidence"]
    E_dict = {}
    for info in ["trustor", "trustee", "evidence"]:
        E_dict[info] = eval(info)
    y = json.dumps(E_dict)
    payload = y.encode('ascii')
    print("\nSending: Trust_Evidence to [...%s]"%(str(delegator_IP.split(':', 4)[4])))

    request = Message(code=GET, payload=payload, uri=f'coap://[{delegator_IP}]/Trust_Evidence')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))
    response_data = json.loads(response.payload)

    # Calculate Trust Value
    evidence_averages = {}
    print('\nCalculating Trust Value')
    trustor = response_data["trustor"]
    trustee = response_data["trustee"]
    for key_name, key_value in response_data.items():
        # Skip trustor and trustee fields
        if key_name in ["trustor", "trustee"]:
            continue
        # Handle both single values and lists
        if isinstance(key_value, (list, tuple)):
            values = key_value
        else:
            values = [key_value]  # Convert single value to list
        numeric_values = []
        for value in values:
            numeric_values.append(float(value))
            average = statistics.fmean(numeric_values)
        evidence_averages[key_name] = average

    E_avg_value = evidence_averages
    #print(E_avg_value)   

    #Trust model
    Score_Response_time =1
    Score_distance =1
    Score_packet_loss_rate = 1
    
    if E_avg_value["response_time"] < 150: 
        Score_Response_time = 1
    elif E_avg_value["response_time"] > 151 and E_avg_value["response_time"] < 400 :
        Score_Response_time = 0.5
    elif E_avg_value["response_time"] >= 400 :
        Score_Response_time = 0
        
    if E_avg_value["distance"] == 0:
        Score_distance = 1
    elif E_avg_value["distance"] == 1:
        Score_distance = 0.5
    elif E_avg_value["distance"] >= 2 :
        Score_distance = 0
        
    if E_avg_value["packet_loss_rate"] < 2:
        Score_packet_loss_rate = 1
    elif E_avg_value["packet_loss_rate"] >= 2 and E_avg_value["packet_loss_rate"] <= 5 :
        Score_packet_loss_rate = 0.5
    elif E_avg_value["packet_loss_rate"] > 5 :
        Score_packet_loss_rate = 0
    W1 = 1/3
    W2 = 1/3
    W3 = 1/3
    Trust_value = ((W1*Score_Response_time)+(W2*Score_distance)+(W3*Score_packet_loss_rate))
    Trust_value= str(f'{Trust_value:.2f}')
    x = {}
    for info in ["trustor", "trustee","Trust_value"]:
            x[info] = eval(info)
    y = json.dumps(x)
    payload = y.encode('ascii')
    print("\nSending: Trust_value_Storage to [...%s]"%(str(delegator_IP.split(':', 4)[4])))
    request = Message(code=POST, payload=payload, uri=f'coap://[{delegator_IP}]/Trust_value_Storage')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))


async def run(protocol, delegate_IP, data): 
    trustor = data["trustor"]
    trustee = data["trustee"]
    IP = trustor,trustee
    
    # Collect Evidence 
    print('\nCollecting Trust Evidence - delegate[...%s]'%(str(trustee.split(':', 4)[4])))
    tasks = [asyncio.create_task(distance(IP)), asyncio.create_task(packet_loss_rateF(IP)), asyncio.create_task(response_time(IP))]
    await asyncio.wait(tasks)

    # Send Evidence to a delegate for storage
    sending_time = "Immediate Send"
    await Send_evidence_to(protocol, delegate_IP, data, sending_time)
    
    # Retrive Evidence from a delegate 
    # Update trust value
    # Send trust value to a delegate for storage
    print('\nRetriving Evidence from delegate[...%s]'%(str(delegate_IP.split(':', 4)[4])))
    print('\nSending Trust_value_Storage to delegate[...%s]'%(str(delegate_IP.split(':', 4)[4])))
    await GetEvidence_UpdateTrust_SendTrust_to(protocol, delegate_IP, data)

    
    # Retrive trust value
    await Get_trust_value_from(protocol, delegate_IP, data)
    print("\nSleep 5s")
    await asyncio.sleep(5) 
    
    #measure resources
    #subprocess.run(['sudo','sh', 'cpu_usage_ps.sh'],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        


async def main(arg):
    #########################################################
    # The below setup is for Delegating Evidence Storage
    #########################################################
    node = int(arg)
    TSS = "2a01:4b00:ea2e:ed00:df88:9855:c51f:3af9"
    delegate_IP="2001:db8:1234:11:62ff:314d:6996:14f9" # suppose to be
 
    # Generate trustee for experiment. We can add all info of trustees here 
    all_trustee = []
    all_trustee2 = []
    for i in range(0, node):
        trustor = "2001:db8:1234:11:bd9c:46e5:537c:94ec"
        trustee = "2001:db8:1234:11:9eb:ca6a:6676:d4c3"
        Trust_computer_IP = "" 
        lease_time = 86400
        evidence = ["distance","packet_loss_rate","response_time"]
        share = 1
        
        x = {}
        for info in ["trustor", "trustee","Trust_computer_IP","lease_time","evidence","share"]:
            x[info] = eval(info)
        all_trustee.append(x)

          
    """
    #Find delegator(s) from TSS
    print('Sending a request to a TSS (%s) for Looking up delegator(s) for %s'%(TSS, delegate_spec["roles"]))
    Delegates= asyncio.run(find_delegates(delegate_spec,TSS))
    aList = json.loads(Delegates)
    TC_IPlist=aList["TC"]
    TR_IPlist=aList["TR"]
    EC_IPlist=aList["EC"]
    DM_IPlist=aList["DM"]
    D_all_Delegates=set(TC_IPlist) & set(TR_IPlist) & set(EC_IPlist) & set(DM_IPlist) # find a delegate that can do all roles
    D_all_Delegates = list(D_all_Delegates) # convert set to list
    print("\nDelegator(s): ")
    print('\n'.join(D_all_Delegates))
    IP_delegate=random.choice(D_all_Delegates)
    """
    # Delegate Trust Repositor
    protocol = await Context.create_client_context()
    await Delegate_Trust_Repositor(protocol,delegate_IP, all_trustee)

    time.sleep(1)
    # loop to create tasks for all trustees
    tasks = []
    for data in all_trustee:
        task = asyncio.create_task(run(protocol,delegate_IP, data))
        tasks.append(task)
    # Wait for all tasks to complete
    if tasks:
        await asyncio.gather(*tasks)
    
   

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
