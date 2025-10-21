#!/usr/bin/env python3
from datetime import datetime
import logging
import json
import sqlite3
import asyncio
import uuid
import string
import statistics
import time
import subprocess
import sys
import multiprocessing
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from E_collector import *
def Query_evidence(i,trustor_ip,trustee_ip, evidence):
    Query_result = []
    E_dict = {}
    #print('[%s][...%s] Updating trust value'%(i,str(trustee_ip.split(':', 4)[4])))
    #print(evidence)
    #await asyncio.sleep(0)
    evidence_list = evidence
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/evidence.db')
    for p in evidence_list:
        if p == "response_time":
            Response_time_list=[]
            #print('Querying %s'%(p))
            sql1 = "select response_time from response_time where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql1):
                Response_time_list.append(row[0]) 
            if len(Response_time_list) == 0:
                avg_response_time=0
                continue
            avg_response_time = statistics.mean(Response_time_list)
            Query_result.append(avg_response_time)
            E_dict[p]=Response_time_list
        elif p == "availability":
            #print('Querying %s'%(p))
            availability_list=[]
            sql2 = "select availability from availability where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                availability_list.append(row[0])
            if len(availability_list) == 0:
                Score_availability = 0.5
                continue
            count = availability_list.count(1)
            Score_availability= count/len(availability_list)
            Query_result.append(Score_availability)
            E_dict[p]=availability_list
        elif p == "task_completion_rate":
            #print('Querying %s'%(p))
            task_completion_rate_list=[]
            sql2 = "select task_completion_rate from task_completion_rate where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                task_completion_rate_list.append(row[0])
            if len(task_completion_rate_list) == 0:
                Score_task_completion_rate=0.5
                continue
            count = task_completion_rate_list.count(1)
            Score_task_completion_rate= count/len(task_completion_rate_list)
            Query_result.append(Score_task_completion_rate)
            E_dict[p]=task_completion_rate_list
        elif p == "distance":
            #print('Querying %s'%(p))
            distance_list=[]
            sql2 = "select distance from distance where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                distance_list.append(row[0])
            if len(distance_list) == 0:
                avg_distance=0
                continue
            avg_distance = statistics.mean(distance_list)
            Query_result.append(avg_distance)
            E_dict[p]=distance_list
        elif p == "packet_loss_rate":
            #print('Querying %s'%(p))
            packet_loss_rate_list=[]
            sql2 = "select packet_loss_rate from packet_loss_rate where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                packet_loss_rate_list.append(row[0])
            if len(packet_loss_rate_list) == 0:
                avg_packet_loss_rate=0
                continue
            avg_packet_loss_rate = statistics.mean(packet_loss_rate_list)
            Query_result.append(avg_packet_loss_rate)
            E_dict[p]=packet_loss_rate_list
        elif p == "honesty":
            #print('Querying %s'%(p))
            honesty_list=[]
            sql2 = "select honesty from honesty where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                honesty_list.append(row[0])
            if len(honesty_list) == 0:
                Score_honesty=0.5
                continue
            count = honesty_list.count(1)
            Score_honesty= count/len(honesty_list)
            Query_result.append(Score_honesty)
            #honesty = statistics.mean(honesty_list)
            E_dict[p]=honesty_list
        elif p == "network_latency":
            #print('Querying %s'%(p))
            network_latency_list=[]
            sql2 = "select network_latency from network_latency where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                network_latency_list.append(row[0])
            if len(network_latency_list) == 0:
                avg_network_latency=0
                continue
            avg_network_latency = statistics.mean(network_latency_list)
            Query_result.append(avg_network_latency)
            E_dict[p]=network_latency_list
        elif p == "cooperativeness":
            #print('Querying %s'%(p))
            cooperativeness_list=[]
            sql2 = "select cooperativeness from cooperativeness where trustor_ip = %s AND trustee_ip = %s " %(repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                cooperativeness_list.append(row[0])
            if len(cooperativeness_list) == 0:
                Score_cooperativeness=0.5
                continue
            Score_cooperativeness = statistics.mean(cooperativeness_list)
            Query_result.append(Score_cooperativeness)
            E_dict[p]=cooperativeness_list
    #print(E_dict)   
    conn.close()
    return Query_result

def Update_trust_value_to_database(i,trustor_ip,trustee_ip, Trust_value):
    #update trust value in database
    conn = sqlite3.connect('/home/pi/aiocoap/smart_traffic/DB/trust.db')
    cur = conn.cursor()
    sql3 = "select count(*) as count from trust_value where trustor_ip = %s AND trustee_ip = %s" %(repr(trustor_ip), repr(trustee_ip))
    cur.execute(sql3)
    numberOfRows = cur.fetchone()[0]
    if numberOfRows> 0:
        conn.execute("UPDATE trust_value set trust_value = ? where trustor_ip = ? AND trustee_ip = ?;",(Trust_value, trustor_ip,trustee_ip))  
        conn.commit()
    else:
        conn.execute("INSERT INTO trust_value (trustor_ip, trustee_ip,trust_value) VALUES (?,?,?)",(trustor_ip, trustee_ip ,Trust_value))
        conn.commit()
    conn.close()
    print('[Trust Update]Update trust Trustee[...%s] VALUE = %s '%(str(trustee_ip.split(':', 4)[4]), Trust_value))

def Update_trust(i,trustor_ip,trustee_ip, evidence,Trust_model):
    #trust relationship between end nodes
    Query_result = Query_evidence(i,trustor_ip,trustee_ip, evidence)
    
    #trust model
    if Trust_model == "T1":
        Score_honesty = Query_result[0]
        Score_cooperativeness = Query_result[1]
        avg_network_latency= Query_result[2]
        Score_network_latency =0.5
        if avg_network_latency < 50:
            Score_network_latency = 1
        elif avg_network_latency >= 50 and avg_network_latency <= 100 :
            Score_network_latency = 0.5
        elif avg_network_latency > 100 :
            Score_network_latency = 0 
        W1 = 1/3
        W2 = 1/3
        W3 = 1/3
        Trust_value = ((W1*Score_network_latency)+(W2*Score_honesty)+(W3*Score_cooperativeness))
    
    elif Trust_model == "T2": 
        Score_availability = Query_result[0]
        Score_task_completion_rate = Query_result[1]
        avg_response_time = Query_result[2]
        Score_response_time =0.5
        if avg_response_time < 150:
            Score_response_time = 1
        elif avg_response_time >= 151 and avg_response_time <= 400 :
            Score_response_time = 0.5
        elif avg_response_time > 401 :
            Score_response_time = 0 
        W1 = 1/3
        W2 = 1/3
        W3 = 1/3
        Trust_value = ((W1*Score_availability)+(W2*Score_task_completion_rate)+(W3*Score_response_time))
    Trust_value= round(Trust_value,2)
    Update_trust_value_to_database(i,trustor_ip,trustee_ip, Trust_value)    
    
    
    
        
async def runn(trustor,trustee,evidence,Trust_model):  
    IP=trustor,trustee
    for i in range(1, 2):
        tasks=[]
        #print("\n[%d]"%(i))   
        for Evidence_name in evidence:
            tasks.append(asyncio.create_task(eval(Evidence_name)(i,IP)))
        #tasks = [asyncio.create_task(honesty(i,IP)), asyncio.create_task(network_latency(i,IP)), asyncio.create_task(cooperativeness(i,IP))]
        await asyncio.wait(tasks)
        Update_trust(i,trustor, trustee,evidence,Trust_model)
        print('[Trust Update]Sleep 1s Trustee[...%s]'%(str(trustee.split(':', 4)[4])))
        #time.sleep(1)

def run(trustor,trustee,evidence,Trust_model):
    asyncio.run(runn(trustor,trustee,evidence,Trust_model))
    
async def main(arg1,arg2):
    
    trustor=[]
    end_nodes=[]
    fog_nodes=[]
    
    endnode = 0
    fognode = int(arg2)
    print("Number of end nodes: %s"%arg1)
    print("Number of fog nodes: %s"%arg2)
    trustor = "2a01:4b00:d119:1c00:393f:f4e:aba6:633f"
    for i in range(0, endnode):
        end_nodes.append("2a01:4b00:d119:1c00:89d9:bc2e:44de:6c"+str(i+10))
    evidence = ["honesty","cooperativeness","network_latency"]
    for i in range(0, fognode):
        fog_nodes.append("2a01:4b00:d119:1c00:925c:8c0f:6fd1:2f"+str(i+10))
    evidence2 = ["availability","task_completion_rate","response_time"]

    tasks=[]
    for p in range(0, endnode):
        t = threading.Timer(0.01, run,args=[trustor,end_nodes[p],evidence,"T1"])
        t.start() 
        tasks.append(t)
    for p in range(0, fognode):
        t = threading.Timer(0.01, run,args=[trustor,fog_nodes[p],evidence2,"T2"])
        t.start() 
        tasks.append(t)   
    for i in range(0, endnode+fognode):
        tasks[i].join()       
    #time.sleep(1)
    #measure resources
    subprocess.run(['sudo','sh', '/home/pi/aiocoap/smart_traffic/locally/cpu_usage_ps.sh'],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
if __name__ == "__main__":
    asyncio.run(main(sys.argv[1],sys.argv[2]))
