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

from Delegate_Evidence_Collector import Delegate_Evidence_Collector
from Evidence_Storage import Evidence_Storage


async def main(arg):
    #########################################################
    # The below setup is for Delegating evidence collector
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
        Trust_repositor_IP = "" 
        lease_time = 86400
        evidence= ["distance","packet_loss_rate","response_time"]
        
        x = {}
        x2 = {}
        for info in ["trustor", "trustee","Trust_repositor_IP","lease_time","evidence"]:
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
    global root
    root = resource.Site()
    root.add_resource(['Evidence_Storage'], Evidence_Storage())
    context = await aiocoap.Context.create_server_context(root)

    protocol = context
    await Delegate_Evidence_Collector(protocol,delegate_IP, all_trustee)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
