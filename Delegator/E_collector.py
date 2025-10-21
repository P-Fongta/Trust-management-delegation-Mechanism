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

DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"
async def distance(IP):
    trustor=IP[0]
    trustee=IP[1]
    
    print("[...%s] Measuring Distance"% (str(trustee.split(':', 4)[4])) )
    #await asyncio.sleep(0)
    #cmd = "sudo traceroute -I -m 10 %s  | awk 'END{print $1}'"%trustee
    #result = subprocess.check_output(cmd,shell=True)
    #hop = int(result.decode()[0])-1   
    hops = traceroute(trustee, max_hops=10, interval=0.05)
    hop=len(hops)-1
    print("[...%s] hop count: %s" % (str(trustee.split(':', 4)[4]),hop))
    conn = sqlite3.connect(DB_Trust_evidence)
    conn.execute("INSERT INTO Trust_evidence (trustor_ip,trustee_ip,Evidence_name, Evidence_value)  VALUES (?,?,?,?)",(trustor,trustee, "distance",hop))
    conn.commit()
    conn.close() 
    
async def packet_loss_rateF(IP):
    trustor=IP[0]
    trustee=IP[1]
    print("[...%s] Measuring packet loss rate" %(str(trustee.split(':', 4)[4]) ))
    #await asyncio.sleep(0)
    """
    process = subprocess.Popen(['ping','-c','10',trustee],stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    packet_loss = float([x for x in stdout.decode('utf-8').split('\n') if x.find('packet loss') != -1][0].split('%')[0].split(' ')[-1])
    """
    host = await async_ping(trustee, count=10, interval=1, timeout=2, privileged=False)
    packet_loss= ((host.packets_sent - host.packets_received)/host.packets_sent)*100
    #print("sent : %s  Received: %s"%(host.packets_sent,host.packets_received))
    print("[...%s] packet loss: %s percent" %(str(trustee.split(':', 4)[4]),packet_loss))
    #print("packet loss: %s percent" % host.packet_loss)
    conn = sqlite3.connect(DB_Trust_evidence)
    conn.execute("INSERT INTO Trust_evidence (trustor_ip,trustee_ip,Evidence_name, Evidence_value)  VALUES (?,?,?,?)",(trustor,trustee, "packet_loss_rate",packet_loss))
    conn.commit()
    conn.close() 
    
async def availability(IP):
    trustor=IP[0]
    trustee=IP[1]
    print("Measuring Availability of: " + trustee )
    await asyncio.sleep(0)
    host = ping(trustee, count=4, interval=0.1, timeout=2, privileged=False)
    print("Availability: %s" % (host.is_alive))
    conn = sqlite3.connect(DB_Trust_evidence)
    conn.execute("INSERT INTO Trust_evidence (trustor_ip,trustee_ip,Evidence_name, Evidence_value)  VALUES (?,?,?,?)",(trustor,trustee, "availability",host.is_alive))
    conn.commit()
    conn.close() 

async def task_completion_rate(IP):   
    trustor=IP[0]
    trustee=IP[1]
    print("[...%s] Measuring task completion rate"%str(trustee.split(':', 4)[4]) )
    await asyncio.sleep(0)
    t_list=[]
    Port = 4000
    Addr = (trustee,Port,0,0)
    msg="Hello"
    num_req=1
    recv=0
    # Create socket
    
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        s.settimeout(1) 
        st = time.time()
        s.sendto(msg.encode(),Addr)
        
        try:
            
            data, address = s.recvfrom(1024)
            et = time.time()
            await asyncio.sleep(0)
            print("task completion rate: response received")
            recv=1
            rep_time = str(f'{(et - st)*1000:.2f}')
            print("response time: %s ms" %rep_time)            
        except socket.timeout: 
            print("task completion rate: Didn't receive any response! [Timeout]")
            recv=0
            rep_time = 2000
            print("response time: %s s" %rep_time)
        finally:
            s.close()
 
    conn = sqlite3.connect(DB_Trust_evidence)
    conn.execute("INSERT INTO Trust_evidence (trustor_ip,trustee_ip,Evidence_name, Evidence_value)  VALUES (?,?,?,?)",(trustor,trustee, "task_completion_rate",recv))
    conn.commit()
    conn.execute("INSERT INTO Trust_evidence (trustor_ip,trustee_ip,Evidence_name, Evidence_value)  VALUES (?,?,?,?)",(trustor,trustee, "response_time",rep_time))
    conn.commit()
    conn.close() 
    
async def response_time(IP):
    trustor=IP[0]
    trustee=IP[1]
    t_list=[]
    Port = 4000
    Des = trustee
    Addr = (Des,Port,0,0)
    msg="37.5"
    response_time = 0
    print("[...%s] Measure response time"%(str(trustee.split(':', 4)[4])))   
    # Create socket
    x=0
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        try:
            s.settimeout(2)
            start_time = time.time_ns()
            #print("[R%s]Sending message..."%x)
            s.sendto(msg.encode(),Addr)
            data, address = s.recvfrom(1024)
            end_time = time.time_ns()
            response_time = (end_time - start_time)
            response_time = round((response_time/1000000),2)
            #print("[R%s]Response Msg :"%x +str(data.decode()))
            print("[...%s] response time = %f ms"% (str(trustee.split(':', 4)[4]),response_time))
            x=x+1
        except Exception as e:
            print(e)
            #exit(0)
            
    conn = sqlite3.connect(DB_Trust_evidence)
    conn.execute("INSERT INTO Trust_evidence (trustor_ip,trustee_ip,Evidence_name, Evidence_value)  VALUES (?,?,?,?)",(trustor,trustee, "response_time",response_time))
    conn.commit()
    conn.close()     
        
async def E_colletor_main():
    IP="2a01:4b00:ea2e:ed00:80:2c25:5944:3dc3","2a01:4b00:ea2e:ed00:df88:9855:c51f:3af9"

    tasks = [response_time(IP),distance(IP),packet_loss_rate(IP)]
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