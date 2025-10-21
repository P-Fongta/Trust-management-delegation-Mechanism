import multiprocessing
import logging
import asyncio
import json
import time
import random
import aiocoap.resource as resource
import aiocoap
from aiocoap import *
import socket
import struct
import sys
import getopt
import threading
import subprocess

# logging setup
#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)
class TSS_DISCOVERY(resource.Resource):
    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        #print(request.payload)
        local_IP = subprocess.getoutput("ip -6 addr show scope global dynamic mngtmpaddr up|egrep -o '([0-9a-f:]+:+)+[0-9a-f]+'")
        payload=local_IP
        payload = payload.encode('ascii')
        print("\nRecv: TSS_Discovery from {}".format(request.remote.hostinfo))

        print("Resp: Reply to {}".format(request.remote.hostinfo))
        #print("{}".format(request))
        return aiocoap.Message(payload=payload)
    
async def push():
    local_addr = "::" #localhost
    mcast_addr = "ff02::fd" #Multicast Address
    mcast_port = 5683 
    ifn = "eth0" #network interface
    payload=""
    
    print("Starting PUSH TSS Discovery method...")
    protocol = await Context.create_client_context()
    while True:  
        # Create a request message
        local_IP = subprocess.getoutput("ip -6 addr show scope global dynamic mngtmpaddr up|egrep -o '([0-9a-f:]+:+)+[0-9a-f]+'")
        payload=local_IP
        payload = payload.encode('ascii')
        request = Message(code=PUT,mtype=1,mid=None,payload=payload, uri='coap://[ff02::fd]/TSS_DISTRIBUTION')
        try:
            await asyncio.wait_for(send_request(protocol,request), timeout=1.0)    
        except asyncio.TimeoutError:
            print('')
        #await protocol.shutdown()

        #print('Result: %s\n%r'%(response.code, response.payload))
        #print(request.encode())
        print("Sending: TSS_Distribution to {}:{}".format(request.unresolved_remote,mcast_port))
        print("{}".format(request))
        await asyncio.sleep(10) 
        #time.sleep(5)
    #sock.sendto(request.encode(), sock_addr)
    '''while True:
        data, sender = sock.recvfrom(1024)
        print("From " + str(sender[0]) + ": " + str(decode(data)))'''
    #await asyncio.sleep(2)     
    #await asyncio.get_running_loop().create_future()
def send_request(protocol,request):
    return protocol.request(request).response

async def pull():
    
    local_addr = "::" #localhost
    mcast_addr = "ff02::fd" #Multicast Address
    mcast_port = 5684 
    ifn = "eth0" #network interface
    print("Starting PULL TSS Discovery method... Waiting for TSS_Discovery")
    # Resource tree creation
    global root
    root = resource.Site()
    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['TSS_DISCOVERY'], TSS_DISCOVERY())
    await aiocoap.Context.create_server_context(root,bind=('::', 5684))
    #await aiocoap.Context.create_server_context(root)
    #note that greater than ff02::fd multicast address the server must join multicast group. otherwise send multicasst via ff08::fd
    #MLD is mandated for addresses with scope 2 (link-scope) or greater. 
    # Create socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # Set multicast interface
    ifi = socket.if_nametoindex(ifn)
    ifis = struct.pack("I", ifi)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, ifis)
    # Set multicast group to join
    group = socket.inet_pton(socket.AF_INET6, mcast_addr) + ifis
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, group)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)
    sock_addr = socket.getaddrinfo(local_addr, mcast_port, socket.AF_INET6, socket.SOCK_DGRAM)[0][-1]
    #sock.bind(sock_addr) 
    await asyncio.get_running_loop().create_future()
    
async def main():  
    task1 = asyncio.create_task(push())
    task2 = asyncio.create_task(pull())
    await task1
    await task2
   
if(__name__=='__main__'):
    asyncio.run(main())
    print('START')