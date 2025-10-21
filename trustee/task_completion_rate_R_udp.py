#Delegate
from datetime import datetime
import time
import random
import socket
import struct
import sys
import getopt
import asyncio
from time import ctime

async def main():
    st = time.process_time()
    x=0
    Port = 4000
    Host = "::"
    Addr = (Host,Port)
    msg="Hello reply"
    i=0
       
    # Create socket
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((Host, Port))
        print(f'socket binded to {Port}')
        print("Waiting for connection...")

        while True:
            status=random.choices([0,1],weights=(0.5,0.5))
            print("\nStatus: "+str(status))
            data, address = s.recvfrom(1024)
            print('...connected from:', address)
            #print(" Receive "+str(data)+" From "+str(address))
          
            if not data:
                break
            time.sleep(1)
            if status[0]==1:
                print("Send "+str(msg)+" To "+str(address))
                s.sendto(msg.encode(),address)
            else:
                continue
            i=i+1  
    s.close()
       
if __name__ == "__main__":
    asyncio.run(main())
