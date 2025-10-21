#Delegate
from datetime import datetime
import time
import random
import socket
import struct
import sys
import getopt
import asyncio
import sqlite3
import json
from time import ctime

async def main():
    st = time.process_time()
    x=0
    Port = 4001
    Host = "::"
    Addr = (Host,Port)
    msg=""
    i=0 
    # Create socket
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.bind((Host, Port))
        print(f'socket binded to {Port}')
        print("Waiting for connection...")
        while True:
            print("\n%d "%i, end = '')
            data, address = s.recvfrom(1024)
            print('...connected from: [...%s] Msg: %s'%(str(address[0].split(':', 4)[4]),str(data.decode())))
            
            if(data.decode() == "vehicle_state_info"):
                msg = {"speed":65, "heading":"north", "location":"55.864,-4.251"}
                payload = json.dumps(msg)
                print("Sending... Msg: %s "%(msg))
                s.sendto(payload.encode(),address)
            elif(data.decode() == "friend_list"):
                msg=["2a01:4b00:d119:1c00:89d9:bc2e:44de:abc6", "2a01:4b00:d119:1c00:89d9:bc2e:44de:abc2", "2a01:4b00:d119:1c00:89d9:bc2e:44de:abc3", "2a01:4b00:d119:1c00:89d9:bc2e:44de:abc4"]
                payload = json.dumps(msg)
                print("Sending... Msg: %s "%(payload))
                s.sendto(payload.encode(),address)
            i=i+1
       
    s.close()
       
if __name__ == "__main__":
    asyncio.run(main())
