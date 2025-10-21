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
    Port = 4000
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
        conn = sqlite3.connect('../DB/report.db')
        while True:
            print("\n%d "%i, end = '')
            data, address = s.recvfrom(1024)
            print('...connected from: [...%s] Msg: %s'%(str(address[0].split(':', 4)[4]),str(data.decode())))
            if(data.decode() == "break down"):
                msg = "Reported"
                print("Sending... Msg: %s "%(msg))
                conn.execute("INSERT INTO broken_down_vehicles (device_ip, msg)  VALUES (?,?)",(address[0], data.decode()))
                conn.commit()
                s.sendto(msg.encode(),address)
            elif 'speed' in data.decode():
                msg="Reported"
                print("Sending... Msg: %s "%(msg))
                data = json.loads(data)
                speed = data["speed"]
                location = data["location"]
                dest = data["dest"]
                conn.execute("INSERT INTO V_state (device_ip, speed,location,dest)  VALUES (?,?,?,?)",(address[0], speed,location,dest))
                conn.commit()
                time.sleep(random.choice((0.01, 0.02)))
                s.sendto(msg.encode(),address)
            i=i+1
    conn.close() 
    s.close()
       
if __name__ == "__main__":
    asyncio.run(main())
