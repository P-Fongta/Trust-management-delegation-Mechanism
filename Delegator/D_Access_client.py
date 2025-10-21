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



async def Grant_Permission(protocol,Trust_repositor_IP, Grant_Permission):


    print('\nSending: Grant_Permission to [...%s]'%str(Trust_repositor_IP.split(':', 4)[4]))
    y = json.dumps(Grant_Permission)
    payload = y.encode('ascii')
    request = Message(code=POST, payload=payload, uri=f'coap://[{Trust_repositor_IP}]/Grant_Permission')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(Trust_repositor_IP.split(':', 4)[4]), response.code))

async def Revoke_Permission(protocol,Trust_repositor_IP, Revoke_Permission):


    print('\nSending: Revoke_Permission to [...%s]'%str(Trust_repositor_IP.split(':', 4)[4]))
    y = json.dumps(Revoke_Permission)
    payload = y.encode('ascii')
    request = Message(code=DELETE, payload=payload, uri=f'coap://[{Trust_repositor_IP}]/Revoke_Permission')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(Trust_repositor_IP.split(':', 4)[4]), response.code))
    


async def main():
    #########################################################
    # The below setup is for Access Permission
    #########################################################
    TSS = "2a01:4b00:ea2e:ed00:df88:9855:c51f:3af9"
    Trust_repositor_IP="2001:db8:1234:11:62ff:314d:6996:14f9" # suppose to be
 
    # Permission here
    Grant_Permission = {
    'trustor': '2001:db8:1234:11:bd9c:46e5:537c:94ec',
    'Trust_evidence_collector': ['2001:db8:1234:11:9eb:ca6a:6676:d4c0', ['', 'I']],
    'Trust_computer_decision-maker': ['2001:db8:1234:11:9eb:ca6a:6676:d4c01', ['RI', 'R']]
    }

    Revoke_Permission = {
    'trustor': '2001:db8:1234:11:bd9c:46e5:537c:94ec'
    }



          
    # Delegate Trust Repositor
    protocol = await Context.create_client_context()
    await Grant_Permission(protocol,Trust_repositor_IP, Grant_Permission)

    #await Revoke_Permission(protocol,Trust_repositor_IP, Revoke_Permission)
    

if __name__ == "__main__":
    asyncio.run(main())
