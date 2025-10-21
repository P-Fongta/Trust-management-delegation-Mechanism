
from datetime import datetime
import logging
import asyncio
import json
from aiocoap import *
import subprocess
import aiocoap
from Service_discovery_client import lookup

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def Handover_Request(protocol,New_delegate_IP, x):

    y = json.dumps(x)

    payload = y.encode('ascii')
    request = Message(code=POST, payload=payload, uri=f'coap://[{New_delegate_IP}]/Handover_Request')
    print("\nSending: Handover_Request to {}".format(request.unresolved_remote))
    response = await protocol.request(request).response
    payload = response.payload.decode('ascii')
    print('\nRecv: from %s Result: %s - %s'%(response.unresolved_remote, response.code, payload))

async def main():
    """
    #########################################################
    # The below setup is for Delegating Evidence Storage
    #########################################################
    node = int(arg)
    TSS = "2a01:4b00:ea2e:ed00:df88:9855:c51f:3af9"
    delegate_IP="2001:db8:1234:11:62ff:314d:6996:14f9" # suppose to be
    local_IP = subprocess.getoutput("ip -6 addr show scope global dynamic mngtmpaddr up|egrep -o '([0-9a-f:]+:+)+[0-9a-f]+'")
 
    # Generate trustee for experiment. We can add all info of trustees here 
    all_trustee = []
    all_trustee2 = []
    for i in range(0, node):
        trustor = local_IP 
        trustee = "2001:db8:1234:11:9eb:ca6a:6676:d4c3"
        Trust_computer_IP = "" 
        lease_time = 86400
        evidence = ["distance","packet_loss_rate","response_time"]
        share = 1
        
        x = {}
        for info in ["trustor", "trustee","Trust_computer_IP","lease_time","evidence","share"]:
            x[info] = eval(info)
        all_trustee.append(x)
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
    """

    TSS_IP = "2001:db8:1234:11:9eb:ca6a:6676:d4c3" 
    delegate_IP="2001:db8:1234:11:62ff:314d:6996:14f9"
    delegator_IP = subprocess.getoutput("ip -6 addr show scope global | awk '/inet6/ {print $2}' | cut -d/ -f1")
    protocol = await Context.create_client_context()
    
    #lookup new delegates
    delegate_spec = {
      "roles":  ["TR"],
      "t_model": ["fuzzy-logic"],
      "e_storage": ["distance"],
      "e_collector": ["distance"] ,
      "d_maker": []
    }
    delegate_nodes =  await lookup(TSS_IP, delegator_IP, delegate_spec)
    #show new delegates
    for role, ip_list in delegate_nodes.items():
        if role in delegate_spec["roles"]:
            if ip_list:
                print(f"{role}: {ip_list}")
            else:
                print(f"{role}: No delegates")

    New_delegate_IP = delegate_nodes
    ips = delegate_nodes.get('TR', [])
    New_delegate_IP = ips[0] if ips else None
    print(New_delegate_IP or "No TR delegates")
    
    x = {}
    for info in ["delegate_IP","delegator_IP"]:
        x[info] = eval(info)
    await Handover_Request(protocol, New_delegate_IP, x)

if __name__ == "__main__":
    asyncio.run(main())
