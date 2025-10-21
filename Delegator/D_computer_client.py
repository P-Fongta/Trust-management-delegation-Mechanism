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

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

from Delegate_Trust_Computer import Delegate_Trust_Computer
from Trust_Computer import Trust_Computer

def Get_old_trust_value(data):
    trustor_ip = data["trustor"]
    trustee_ip = data["trustee"]
    trust_value= {}

    conn = sqlite3.connect(DB_Trust_value)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = "select * from Trust_value where trustor_ip = ? AND trustee_ip = ?"
    cur.execute(sql,(trustor_ip,trustee_ip))
    row = cur.fetchone()
    if row: 
        trust_value["trust_value"]= row["trust_value"]
    conn.close()

    return trust_value

async def run(protocol,delegate_IP, data): 
    trustor = data["trustor"]
    trustee = data["trustee"]
    IP = trustor,trustee
    
    

    # Collect Evidence 
    print('\nCollecting Trust Evidence - delegate[...%s]'%(str(trustee.split(':', 4)[4])))
    tasks = [asyncio.create_task(distance(IP)), asyncio.create_task(packet_loss_rateF(IP)), asyncio.create_task(response_time(IP))]
    await asyncio.wait(tasks)

    # Some trust model need old trust value
    Old_trust_value = Get_old_trust_value(data)

    await Trust_Computer(protocol, delegate_IP, data, Old_trust_value)
  
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
        Trust_repositor_IP = ""
        t_model = "fuzzy-logic"
        evidence= ["distance","packet_loss_rate","response_time"]
        share = "0"
        
        x = {}
        for info in ["trustor", "trustee", "lease_time","t_model","Trust_repositor_IP","evidence","share"]:
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
    await Delegate_Trust_Computer(protocol,delegate_IP, all_trustee)

    
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
