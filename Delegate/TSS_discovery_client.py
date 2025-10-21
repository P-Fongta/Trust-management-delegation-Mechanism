# This code is for Delegates, Delegators to discover a TSS by a Push and Pull methods. 
# 
from datetime import datetime
import logging
import json
import sqlite3
import asyncio
import uuid
import time
import random
import aiocoap.resource as resource
import aiocoap
from aiocoap import *
import socket
import struct
import sys
import getopt
# logging setup

#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)
exit_future = None
class TSS_DISTRIBUTION(resource.Resource):
    def __init__(self):
        super().__init__()
    def render(self, request):
        print("\nRecv: TSS_Distribution from {}".format(request.unresolved_remote))
        print("{}\n".format(request))
        print("Resp: No Response")

        #print(request.payload)
        TSS_IP = request.payload.decode()
        print("TSS IP Address: {}".format(TSS_IP))
        exit_future.set_result("Done!")
        return super().render(request)
    async def render_PUT(self, request):
        return aiocoap.message.NoResponse

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


async def main(argv):

    ch=""
    try:
        opts, args = getopt.getopt(argv, "m:")
    except getopt.GetoptError:
        print("TSS_discovery.py -m <push|pull>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-m']:
            ch = arg
        else:
            print("TSS_discovery.py -m <push|pull>")
            sys.exit()
    
    if ch=="push":
        local_addr = "::"
        mcast_addr = "ff02::fd"
        mcast_port = 5683
        ifn = "eth0"
        print("Starting PUSH TSS Discovery method... Waiting for TSS_Distribution ")
        # Resource tree creation
        global root
        root = resource.Site()
        root.add_resource(['.well-known', 'core'],
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(['TSS_DISTRIBUTION'], TSS_DISTRIBUTION())
        await aiocoap.Context.create_server_context(root,multicast=[(mcast_addr, ifn)])
        # Create socket
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Set multicast interface
        ifi = socket.if_nametoindex(ifn)
        ifis = struct.pack("I", ifi)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, ifis)

        # Set multicast group to join
        group = socket.inet_pton(socket.AF_INET6, mcast_addr) + ifis
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, group)

        sock_addr = socket.getaddrinfo(mcast_addr, mcast_port, socket.AF_INET6, socket.SOCK_DGRAM)[0][4]
        
        #data, sender = sock.recvfrom(1024)
        #print(str(sender)+" : "+str(data))
        #print('TSS Discovery message from %s',str(sender))
         
        global exit_future
        exit_future = asyncio.get_running_loop().create_future()
        await exit_future
        # Run forever
        # await asyncio.get_running_loop().create_future()
        """try:# Exit after 10 seconds
            await asyncio.wait_for(asyncio.get_running_loop().create_future(), timeout=10.0)
        except asyncio.TimeoutError:
            print("Timeout reached, exiting...")
        """
        
        
    elif ch=="pull":
        mcast_addr = "ff02::fd"
        pull_port = 5684
        print("Starting PULL TSS Discovery method")
        protocol = await Context.create_client_context()
        request = Message(code=GET, mtype=1, uri=f'coap://[{mcast_addr}]:{pull_port}/TSS_DISCOVERY')
        #print(request.encode())
        print("Sending: TSS_Discovery to Multicast Address {}:{}".format(request.unresolved_remote,pull_port))

        response = await protocol.request(request).response
        #print("{}".format(request))  #show a request message

        print("\nRecv: TSS Reply from {}".format(response.remote.hostinfo))
        TSS_IP = response.payload.decode()
        print("TSS IP Address: {}".format(TSS_IP))
        #print("{}".format(response))  #show a response message
        await asyncio.sleep(5) 
      

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
