from datetime import datetime
import logging
import json
import sqlite3
import asyncio
import uuid
import time
import random
import socket
import struct
import sys
import statistics
import threading
import os
import select
from icmplib import ping
from icmplib import async_ping
from icmplib import traceroute
import subprocess

async def honesty(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    t_list=[]
    Port = 4001
    Des = trustee
    Addr = (Des,Port,0,0)
    msg="vehicle_state_info"
    honesty = 0
    print("[%s][...%s]Measuring honesty"%(i,str(trustee.split(':', 4)[4])))   
    x=0
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.settimeout(2)
            #print("[R%s]Sending message..."%x)
            s.sendto(msg.encode(),Addr)
            data, address = s.recvfrom(1024)
            data = json.loads(data)
            speed_value = int(data["speed"])
            if float(speed_value) >0 and float(speed_value)<70 :
                honesty = 1
            else:
                honesty = 0
            print("[%s][...%s]honesty = %d "% (i,str(trustee.split(':', 4)[4]),honesty))
            x=x+1
        except Exception as e:
            print(e)
            #exit(0)
            
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    conn.execute("INSERT INTO honesty (trustor_ip, trustee_ip,honesty)  VALUES (?,?,?)",(trustor, Des, honesty))
    conn.commit()
    conn.close() 
async def network_latency(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    print("[%s][...%s]Measuring network latency" %(i,str(trustee.split(':', 4)[4]) ))
  
    host = await async_ping(trustee, count=4, interval=0.1, timeout=2, privileged=False)
    latency=host.avg_rtt
    latency = round(latency, 2)
    print("[%s][...%s]Network latency : %s ms " %(i,str(trustee.split(':', 4)[4]),latency))
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    conn.execute("INSERT INTO network_latency (trustor_ip,trustee_ip,network_latency)  VALUES (?,?,?)",(trustor,trustee,latency))
    conn.commit()
    conn.close() 
async def cooperativeness(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    t_list=[]
    Port = 4001
    Des = trustee
    Addr = (Des,Port,0,0)
    myfriend=["2a01:4b00:d119:1c00:89d9:bc2e:44de:abc1", "2a01:4b00:d119:1c00:89d9:bc2e:44de:abc2", "2a01:4b00:d119:1c00:89d9:bc2e:44de:abc3", "2a01:4b00:d119:1c00:89d9:bc2e:44de:abc4"]
    msg="friend_list"
    cooperativeness = 0
    print("[%s][...%s]Measuring cooperativeness"%(i,str(trustee.split(':', 4)[4])))   
    x=0
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.settimeout(2)
            #print("[R%s]Sending message..."%x)
            s.sendto(msg.encode(),Addr)
            data, address = s.recvfrom(1024)
            friend_of_trustee = json.loads(data)
            #calculate common friend
            common_elements = set(myfriend).intersection(set(friend_of_trustee ))
            num_common_elements = len(common_elements)
            # Find the total number of unique elements in both lists
            total_elements = set(myfriend).union(set(friend_of_trustee ))
            num_total_elements = len(total_elements)
            cooperativeness = (num_common_elements / num_total_elements)
            cooperativeness = round(cooperativeness, 2)
            print("[%s][...%s]cooperativeness = %.2f "% (i,str(trustee.split(':', 4)[4]),cooperativeness))
            x=x+1
        except Exception as e:
            print(e)
            #exit(0)
            
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    conn.execute("INSERT INTO cooperativeness (trustor_ip, trustee_ip,cooperativeness)  VALUES (?,?,?)",(trustor, Des, cooperativeness))
    conn.commit()
    conn.close() 
async def distance(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    
    print("\n[%s]Measuring Distance [...%s]"% (i,str(trustee.split(':', 4)[4])) )
    #await asyncio.sleep(0)
    #cmd = "sudo traceroute -I -m 10 %s  | awk 'END{print $1}'"%trustee
    #result = subprocess.check_output(cmd,shell=True)
    #hop = int(result.decode()[0])-1    
    hops = traceroute(trustee, max_hops=10, interval=0.05)
    hop=len(hops)-1
    print("\n[%s]Hop count [...%s] = %s " % (i,str(trustee.split(':', 4)[4]),hop))
    conn = sqlite3.connect('/home/pi/aiocoap/e-health/DB/evidence.db')
    conn.execute("INSERT INTO distance (trustor_ip,trustee_ip,distance)  VALUES (?,?,?)",(trustor,trustee,hop))
    conn.commit()
    conn.close() 
    
async def packet_loss_rate(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    print("\n[%s]Measuring packet loss rate [...%s]" %(i,str(trustee.split(':', 4)[4]) ))
    #await asyncio.sleep(0)
    """
    process = subprocess.Popen(['ping','-c','10',trustee],stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    packet_loss = float([x for x in stdout.decode('utf-8').split('\n') if x.find('packet loss') != -1][0].split('%')[0].split(' ')[-1])
    """
    host = await async_ping(trustee, count=10, interval=0.1, timeout=2, privileged=False)
    packet_loss= ((host.packets_sent - host.packets_received)/host.packets_sent)*100
    #print("sent : %s  Received: %s"%(host.packets_sent,host.packets_received))
    print("\n[%s]Packet loss [...%s]: %s percent " %(i,str(trustee.split(':', 4)[4]),packet_loss))
    #print("packet loss: %s percent" % host.packet_loss)
    conn = sqlite3.connect('/home/pi/aiocoap/e-health/DB/evidence.db')
    conn.execute("INSERT INTO packet_loss_rate (trustor_ip,trustee_ip,packet_loss_rate)  VALUES (?,?,?)",(trustor,trustee,packet_loss))
    conn.commit()
    conn.close() 
    
async def availability(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    print("[%s][...%s]Measuring availability " %(i,str(trustee.split(':', 4)[4]) ))
    host = await async_ping(trustee, count=4, interval=0.1, timeout=2, privileged=False)
    print("[%s][...%s]availability : %s " %(i,str(trustee.split(':', 4)[4]),host.is_alive))
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    conn.execute("INSERT INTO availability (trustor_ip,trustee_ip,availability)  VALUES (?,?,?)",(trustor,trustee,host.is_alive))
    conn.commit()
    conn.close() 

async def task_completion_rate(i,IP):   
    trustor=IP[0]
    trustee=IP[1]
    print("[%s][...%s]Measuring task_completion_rate " %(i,str(trustee.split(':', 4)[4])))
    t_list=[]
    Port = 4000
    Addr = (trustee,Port,0,0)
    msg = "break down"
    num_req=1
    recv=0
    # Create socket
    
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(2)
        s.sendto(msg.encode(),Addr)
        try: 
            data, address = s.recvfrom(1024)
            print("[%s][...%s]task_completion_rate: Received " %(i,str(trustee.split(':', 4)[4])))
            recv=1
        except socket.timeout: 
            print("[%s][...%s]task_completion_rate: Didn't receive any response! [Timeout]" %(i,str(trustee.split(':', 4)[4])))
            recv=0
        finally:
            s.close()
 
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    conn.execute("INSERT INTO task_completion_rate (trustor_ip, trustee_ip, task_completion_rate)  VALUES (?,?,?)",(trustor, trustee ,recv))
    conn.commit()
    conn.close() 
    
async def response_time(i,IP):
    trustor=IP[0]
    trustee=IP[1]
    print("[%s][...%s]Measuring response time " %(i,str(trustee.split(':', 4)[4])))   
    t_list=[]
    Port = 4000
    Des = trustee
    Addr = (Des,Port,0,0)
    msg = {"speed":60, "dest":"52.864,-4.451", "location":"55.864,-4.251"}
    response_time = 0
     
    # Create socket
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(2)
        payload = json.dumps(msg)
        try:
            start_time = time.time_ns()
            s.sendto(payload.encode(),Addr)
            data, address = s.recvfrom(1024)
            end_time = time.time_ns()
            response_time = (end_time - start_time)
            response_time = round((response_time/1000000),2)
            print("[%s][...%s]Response_time  = %.2f ms  "% (i,str(trustee.split(':', 4)[4]),response_time))
        except Exception as e:
            print(e)
            #exit(0)
            
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    conn.execute("INSERT INTO response_time (trustor_ip, trustee_ip,response_time)  VALUES (?,?,?)",(trustor, Des, response_time))
    conn.commit()
    conn.close()     
        
async def E_colletor_main():
    IP="2a01:4b00:d119:1c00:393f:f4e:aba6:633f","2a01:4b00:d119:1c00:89d9:bc2e:44de:6c14"

    tasks = [honesty(1,IP),cooperativeness(1,IP),network_latency(1,IP)]
    #tasks = [response_time(1,IP),task_completion_rate(1,IP),availability(1,IP)]
    await asyncio.wait(tasks)
    
    """
    for p in evidence_name:
        if p == "response_time":
            await response_time(IP)
        elif p == "availability":
            await availability(IP)
        elif p == "task_completion_rate":
            await task_completion_rate(IP)
    """
        

if __name__ == "__main__":
    asyncio.run(E_colletor_main())