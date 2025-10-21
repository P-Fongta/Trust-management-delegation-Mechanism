#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This is a usage example of aiocoap that demonstrates how to implement a
simple server. See the "Usage Examples" section in the aiocoap documentation
for some more information."""
#Delegate
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
class TSS_DISCOVERY(resource.Resource):
    def __init__(self):
        super().__init__()
    def render(self, request):
        print("Request from {} to {}".format(request.remote, request))
        print("Recv: TSS Discovery from {}".format(request.unresolved_remote))
        print("{}".format(request))
        return super().render(request)
        
    async def render_get(self, request):
        
        return aiocoap.message.NoResponse
    async def render_post(self, request):
        
        return aiocoap.message.NoResponse
class TSS_DISTRIBUTION(resource.Resource):
    def __init__(self):
        super().__init__()
    def render(self, request):
        print("\nRecv: TSS Distribution from {}".format(request.unresolved_remote))
        print("{}\n".format(request))
        print("Resp: No Response")
        return super().render(request)
    async def render_get(self, request):
        #print(request.payload)
        
        return aiocoap.message.NoResponse
    async def render_post(self, request):
        #print(request.payload)
        
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
# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main(argv):

    local_addr = "::"
    mcast_addr = "ff03::fd"
    mcast_port = 5683

    ifn = "wlan0"
    payload=""
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
        # Resource tree creation
        global root
        root = resource.Site()
     
        root.add_resource(['.well-known', 'core'],
                resource.WKCResource(root.get_resources_as_linkheader))
        root.add_resource(['TSS_DISTRIBUTION'], TSS_DISTRIBUTION())
        root.add_resource(['TSS_DISCOVERY'], TSS_DISCOVERY())
        await aiocoap.Context.create_server_context(root,multicast=[ifn])
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
         
        
        
        # Run forever
        await asyncio.get_running_loop().create_future()
        
        
    elif ch=="pull":
        mcast_addr_pull = "ff02::fd"
        pull_port = 5683
        protocol = await Context.create_client_context()
 
        request = Message(code=POST, mtype=1,payload=payload.encode(), uri='coap://[ff02::fd]/TSS_DISCOVERY')
        #print(request.encode())
        print("Send: TSS Discovery to {}:{}".format(request.unresolved_remote,pull_port))

        response = await protocol.request(request).response
        print("{}".format(request))
        print("\nResp: TSS Reply from {}".format(request.unresolved_remote))
        print("{}".format(response))
        await asyncio.sleep(5) 
      

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
