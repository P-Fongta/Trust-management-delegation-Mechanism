#!/usr/bin/env python3


from datetime import datetime
import logging
import asyncio
import json
import subprocess
from aiocoap import *
from E_collector import *

from Delegate_Trust_Computer_Repositor import Delegate_Trust_Computer_Repositor
from Send_evidence_to import Send_evidence_to
from Trust_Result import Trust_Result


async def run(protocol,delegate_IP, data): 
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

    # GET trust result
    decision_type = "TD"
    threshold = 0.6
    await Trust_Result(protocol,delegate_IP, data, decision_type, threshold)
        
    """
    #measure resources
    subprocess.run(['sudo','sh', 'cpu_usage_ps.sh'],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("\n[%s]Sleep 1s [...%s]"%(i,str(trustee.split(':', 4)[4])))
    """
    await asyncio.sleep(5)


async def main(arg):
    node = int(arg)
    TSS = "2a01:4b00:ea2e:ed00:df88:9855:c51f:3af9"
    delegate_IP="2001:db8:1234:11:62ff:314d:6996:14f9" # suppose to be
 
    # Generate trustee for experiment. We can add all info of trustees here 
    all_trustee = []
    all_trustee2 = []
    all_trustee3 = []
    for i in range(0, node):
        trustor = "2a01:4b00:ea2e:ed00:2391:df94:11ab:4397"
        trustee = "2001:db8:1234:11:9eb:ca6a:6676:d4c"+str(i)
        lease_time = 86400
        t_model = "weighted sum"
        t_update = "time-driven" 
        evidence= ["distance","packet_loss_rate","response_time"]
        share = "0"
        
        x = {}
        x2 = {}
        x3 = {}
        for info in ["trustor", "trustee", "lease_time","t_model","t_update","evidence","share"]:
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
    await Delegate_Trust_Computer_Repositor(protocol,delegate_IP, all_trustee)

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
