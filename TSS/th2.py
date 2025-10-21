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
class TSS_DISTRIBUTION(resource.Resource):
    def __init__(self):
        super().__init__()
    def render(self, request):
        print("Recv: TSS Distribution from {}".format(request.unresolved_remote))
        print("{}\n".format(request))
        print("Resp: No Response")
        return super().render(request)
    async def render_post(self, request):
        #print(request.payload)
        #payload="Hi"
        #payload = payload.encode('ascii')
        return aiocoap.message.NoResponse
class PrintingLogSite(resource.Resource):
    def render(self, request):
        print("Request from {} to {}".format(request.remote, request.opt.uri_path))
        return super().render(request)      
class TSS_DISCOVERY(resource.Resource):
    def __init__(self):
        super().__init__()
    def render(self, request):
        print("Request from {} to {}".format(request.remote, request.opt.uri_path))
        print("Recv: TSS Discovery from {}".format(request.unresolved_remote))
        print("{}".format(request))
        return super().render(request)
        
    async def render_post(self, request):
        #print(request.payload)
        #payload="Hi"
        #payload = payload.encode('ascii')
        print("\nResp: TSS Reply to {}".format(request.unresolved_remote))
        print("{}".format(request))
        return aiocoap.Message()

def decode(rawdata, remote=None):
    """Create Message object from binary representation of message."""
    try:
        (vttkl, code, mid) = struct.unpack('!BBH', rawdata[:4])
    except struct.error:
        raise error.UnparsableMessage("Incoming message too short for CoAP")
    version = (vttkl & 0xC0) >> 6
    if version != 1:
        raise error.UnparsableMessage("Fatal Error: Protocol Version must be 1")
    mtype = (vttkl & 0x30) >> 4
    token_length = (vttkl & 0x0F)
    msg = Message(mtype=mtype, mid=mid, code=code)
    msg.token = rawdata[4:4 + token_length]
    msg.payload = msg.opt.decode(rawdata[4 + token_length:])
    msg.remote = remote
    return msg

# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)
    
    
async def push():
    local_addr = "::"
    mcast_addr = "ff03::fd"
    mcast_port = 5683
    ifn = "wlan0"
    payload=""
    
    print("Start Push method...")
    protocol = await Context.create_client_context()
    while True:  
        # Create socket a request
        request = Message(code=POST,mtype=1,mid=None,uri='coap://[ff03::fd]/TSS_DISTRIBUTION')
        
        try:
            await asyncio.wait_for(send_request(protocol,request), timeout=1.0)    
        except asyncio.TimeoutError:
            print('timeout!')
        #await protocol.shutdown()

        #print('Result: %s\n%r'%(response.code, response.payload))
        #print(request.encode())
        print("Send: TSS Distribution to {}:{}".format(request.unresolved_remote,mcast_port))
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
    print("Start Pull method...")
    local_addr = "::"
    mcast_addr = "ff02::fd"
    mcast_port = 5683
    ifn = "wlan0"
    # Resource tree creation
    global root
    root = resource.Site()
    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['TSS_DISCOVERY'], TSS_DISCOVERY())
    root.add_resource(['TSS_DISTRIBUTION'], TSS_DISTRIBUTION())
    
    await aiocoap.Context.create_server_context(root,multicast=[ifn])
    #await aiocoap.Context.create_server_context(root)
    #note that ff02::fd multicast the server must join multicast group. otherwise send multicasst via ff16::fe
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