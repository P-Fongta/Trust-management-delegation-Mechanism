"""This is service discovery functions for clients"""

from datetime import datetime
import logging
import asyncio
import json
from aiocoap import *
import subprocess
import aiocoap

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def register(TSS_IP, local_IP, x):
    
    y = json.dumps(x)
    #print(y)
    
    context = await Context.create_client_context()
    #await asyncio.sleep(2)

    payload = y.encode('ascii')
    request = Message(code=POST, payload=payload, uri=f'coap://[{TSS_IP}]/REG_Request')
    print("\nSending: REG_Request to {}".format(request.unresolved_remote))
    print('Payload: %s'%(payload))
    response = await context.request(request).response

    print('\nRecv: from %s \nResult: %s\nRegistration Ref: %s'%(response.unresolved_remote, response.code, response.payload.decode('UTF-8')))
    print("{}".format(response))
    leasing_time = datetime.timestamp(datetime.now())+x['lease_time']
    #print(x["lease_time"])
    f = open("Registration_info.txt", "w")
    f.write(str(TSS_IP)+"\n"+response.payload.decode('UTF-8')+"\n"+str(leasing_time))
    f.close()


async def deregister(TSS_IP, local_IP, deregister):
    
    x = open("Registration_info.txt").read().splitlines()
    print("TSS IP Address: %s\nRegistration Ref: %s\nRegistration expiry: %s"%(x[0],x[1], datetime.fromtimestamp(float(x[2]))))
    deregister['ref']=x[1]
    y = json.dumps(deregister)
    #print(y)
    
    context = await Context.create_client_context()
    #await asyncio.sleep(2)

    payload = y.encode('ascii')
    request = Message(code=DELETE, payload=payload, uri=f'coap://[{TSS_IP}]/DEREG_Request')
    print("Deregister role(s): %s"%deregister["roles"])
    print("Sending: DEREG_Request to {}".format(request.unresolved_remote))
    response = await context.request(request).response
    print('\nRecv: from %s \nResult: %s, %s'%(response.unresolved_remote, response.code, response.payload.decode('UTF-8')))

    #print('Result: %s'%(response.code))

async def lease_renew(TSS_IP, local_IP, lease_time):
    
    
    rdata = open("Registration_info.txt").read().splitlines()
    print("TSS IP Address: %s\nRegistration Ref: %s\nRegistration expiry: %s"%(rdata [0],rdata [1], datetime.fromtimestamp(float(rdata [2]))))
    lease_time['ref']=rdata[1]
    y = json.dumps(lease_time)
    #print(y)
   
    context = await Context.create_client_context()
    #await asyncio.sleep(1)

    payload = y.encode('ascii')
    request = Message(code=PUT, payload=payload, uri=f'coap://[{TSS_IP}]/Lease_Renewal_Request')
    print("Sending: Lease Renew to {}".format(request.unresolved_remote))
    response = await context.request(request).response
    print('\nRecv: from %s \nResult: %s, %s'%(response.unresolved_remote, response.code, response.payload.decode('UTF-8')))
    #print('Result: %s'%(response.code))

async def lookup(TSS_IP, local_IP, delegate_spec):
    
    y = json.dumps(delegate_spec )
    #print(y)
    payload = y.encode('ascii')
    protocol = await Context.create_client_context()

    request = Message(code=GET, payload=payload, uri=f"coap://[{TSS_IP}]/Delegate_Lookup")
    print("Sending: Delegate_Lookup to {}".format(request.unresolved_remote))
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        if response.code == aiocoap.NOT_FOUND:
            print('\nRecv: from %s \nResult: %s, %s'%(response.unresolved_remote, response.code, response.payload.decode('UTF-8')))
        else:
            print('\nRecv: from %s \nResult: %s'%(response.unresolved_remote, response.code))
            delegate_nodes = json.loads(response.payload)
            return delegate_nodes
            for role, ip_list in delegate_nodes.items():
                if role in delegate_spec["roles"]:
                    if ip_list:
                        print(f"{role}: {ip_list}")
                        return delegate_nodes
                    else:
                        print(f"{role}: No delegates")
        #print('Delegate node(s): %s'%(response.payload.decode('UTF-8')))

async def main():
    TSS_IP = "2001:db8:1234:11:9eb:ca6a:6676:d4c3" 
    local_IP = subprocess.getoutput("ip -6 addr show scope global dynamic mngtmpaddr up|egrep -o '([0-9a-f:]+:+)+[0-9a-f]+'")
    """ arguments for Registration
    x = {
      "ip": f'{local_IP}',
      "lease_time": 86400,
      "roles":  ["TC","TR","EC","DM"],
      "t_model": ["weighted sum","fuzzy-logic"],
      "e_storage": ["reliability","latency"],
      "e_collector": ["reliability","job completion rate"],
      "d_maker": ["TD","TBS"],
    }
    """
    
    """ arguments for deregistration
    deregister = {
      "roles":  ["EC"]
    }
    """

    """ arguments for lease renewal
    lease_time = {"lease_time": 86400}
    """

    """ arguments for lookup
    delegate_spec = {
      "roles":  ["TC","TR"],
      "t_model": ["fuzzy-logic"],
      "e_storage": ["distance"],
      "e_collector": [] ,
      "d_maker": ["TD"]
    }
    delegate_nodes =  await lookup(TSS_IP, local_IP, delegate_spec)
    for role, ip_list in delegate_nodes.items():
        if role in delegate_spec["roles"]:
            if ip_list:
                print(f"{role}: {ip_list}")
                return delegate_nodes
            else:
                print(f"{role}: No delegates")
    """
if __name__ == "__main__":
    asyncio.run(main())
