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

def Update_trust(i,trustor_ip,trustee_ip, evidence,Trust_model, Trust_ctrl):
    #trust relationship between end nodes
    Query_result = Query_evidence(i,trustor_ip,trustee_ip, evidence)
    
    #trust model["honesty","cooperativeness","network_latency"]
    if Trust_model == "T1":
        Score_honesty = Query_result[0]
        Score_cooperativeness = Query_result[1]
        avg_network_latency= Query_result[2]
        #compute a trust value by fuzzy logic 
        final_Trust = ctrl.ControlSystemSimulation(Trust_ctrl)
        final_Trust.input[ 'honesty' ] = Score_honesty
        final_Trust.input[ 'cooperativeness' ] = Score_cooperativeness
        final_Trust.input[ 'network_latency' ] = avg_network_latency
        # Crunch the numbers
        final_Trust.compute()
        Trust_value = final_Trust.output['Trust']
    
    elif Trust_model == "T2":
        Score_availability = Query_result[0]
        Score_task_completion_rate = Query_result[1]
        avg_response_time = Query_result[2]
        #compute a trust value by fuzzy logic 
        final_Trust = ctrl.ControlSystemSimulation(Trust_ctrl)
        final_Trust.input[ 'availability' ] = Score_availability
        final_Trust.input[ 'task_completion_rate' ] = Score_task_completion_rate
        final_Trust.input[ 'response_time' ] = avg_response_time
        # Crunch the numbers
        final_Trust.compute()
        Trust_value = final_Trust.output['Trust']
    Trust_value= round(Trust_value,2)
    Update_trust_value_to_database(i,trustor_ip,trustee_ip, Trust_value)    
    
    
    
        
async def runn(trustor,trustee,evidence,Trust_model, Trust_ctrl):  
    IP=trustor,trustee
    for i in range(1, 2):
        tasks=[]
        #print("\n[%d]"%(i))   
        for Evidence_name in evidence:
            tasks.append(asyncio.create_task(eval(Evidence_name)(i,IP)))
        #tasks = [asyncio.create_task(honesty(i,IP)), asyncio.create_task(network_latency(i,IP)), asyncio.create_task(cooperativeness(i,IP))]
        await asyncio.wait(tasks)
        Update_trust(i,trustor, trustee,evidence,Trust_model, Trust_ctrl)
        print('[Trust Update]Sleep 1s Trustee[...%s]'%(str(trustee.split(':', 4)[4])))
        #time.sleep(1)

def run(trustor,trustee,evidence,Trust_model,Trust_ctrl):
    asyncio.run(runn(trustor,trustee,evidence,Trust_model,Trust_ctrl))
    
async def main(arg1,arg2):
    #end node
    #define membership functions and rules of the trust model 
    honesty = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'honesty' )
    cooperativeness = ctrl.Antecedent(np.arange(0, 1.1,0.1), 'cooperativeness' )
    network_latency = ctrl.Antecedent(np.arange(0, 2001, 1), 'network_latency' )
    Trust = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Trust' )

    honesty[ 'low' ] = fuzz.trimf(honesty.universe, [ 0, 0, 0.5])
    honesty[ 'medium' ] = fuzz.trimf(honesty.universe, [0, 0.5, 1])
    honesty[ 'high' ] = fuzz.trimf(honesty.universe, [ 0.5,1,1])

    network_latency[ 'low' ] = fuzz.trapmf(network_latency.universe, [ 0, 0, 30, 50])
    network_latency[ 'medium' ] = fuzz.trapmf(network_latency.universe, [ 30, 40,50, 70])
    network_latency[ 'high' ] = fuzz.trapmf(network_latency.universe, [ 80, 90, 2000, 2000])
    
    cooperativeness[ 'low' ] = fuzz.trimf(cooperativeness.universe, [ 0, 0, 0.5])
    cooperativeness[ 'medium' ] = fuzz.trimf(cooperativeness.universe, [ 0, 0.5, 1])
    cooperativeness[ 'high' ] = fuzz.trimf(cooperativeness.universe, [ 0.5,1,1])

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    Trust[ 'low' ] = fuzz.trimf(Trust.universe, [ 0,0, 0.3])
    Trust[ 'medium' ] = fuzz.trimf(Trust.universe, [ 0.2, 0.5, 0.8])
    Trust[ 'high' ] = fuzz.trimf(Trust.universe, [ 0.7 ,1, 1 ])

    rule1 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'high' ] & network_latency[ 'high' ], Trust[ 'high' ])
    rule2 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'high' ] & network_latency[ 'medium' ] , Trust[ 'high' ])
    rule3 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'high' ] & network_latency[ 'low' ] , Trust[ 'high' ])

    rule4 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'medium' ] & network_latency[ 'high' ] , Trust[ 'medium'  ])
    rule5 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'medium' ] & network_latency[ 'medium' ] , Trust[ 'medium' ])
    rule6 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'medium' ] & network_latency[ 'low' ] , Trust[ 'medium'  ])

    rule7 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'low'  ] & network_latency[ 'high' ] , Trust[ 'low' ])
    rule8 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'low'  ] & network_latency[ 'medium' ] , Trust[ 'medium' ])
    rule9 = ctrl.Rule(honesty[ 'high' ] & cooperativeness[ 'low'  ] & network_latency[ 'low' ] , Trust[ 'high' ])

    rule10 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'high' ] & network_latency[ 'high' ], Trust[ 'low' ])
    rule11 = ctrl.Rule(honesty[ 'medium'] & cooperativeness[ 'high' ] & network_latency[ 'medium' ], Trust[ 'medium'])
    rule12 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'high' ] & network_latency[ 'low' ], Trust[ 'medium' ])

    rule13 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'medium' ] & network_latency[ 'high' ], Trust[ 'medium'])
    rule14 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'medium' ] & network_latency[ 'medium' ], Trust[ 'medium'  ])
    rule15 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'medium' ] & network_latency[ 'low' ], Trust[ 'medium'  ])

    rule16 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'low' ] & network_latency[ 'high' ], Trust[ 'medium' ])
    rule17 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'low' ] & network_latency[ 'medium' ], Trust[ 'medium' ])
    rule18 = ctrl.Rule(honesty[ 'medium' ] & cooperativeness[ 'low' ] & network_latency[ 'low' ], Trust[ 'low' ])

    rule19 = ctrl.Rule(honesty[ 'low' ] & cooperativeness[ 'high' ] & network_latency[ 'high' ], Trust[ 'low' ])
    rule20 = ctrl.Rule(honesty[ 'low'] & cooperativeness[ 'high' ] & network_latency[ 'medium' ], Trust[ 'medium' ])
    rule21 = ctrl.Rule(honesty[ 'low' ] & cooperativeness[ 'high' ] & network_latency[ 'low' ], Trust[ 'high' ])

    rule22 = ctrl.Rule(honesty[ 'low' ] & cooperativeness[ 'medium' ] & network_latency[ 'high' ], Trust[ 'medium' ])
    rule23 = ctrl.Rule(honesty[ 'low' ] & cooperativeness[ 'medium' ] & network_latency[ 'medium' ], Trust[ 'medium' ])
    rule24 = ctrl.Rule(honesty[ 'low'] & cooperativeness[ 'medium' ] & network_latency[ 'low' ], Trust[ 'medium' ])

    rule25 = ctrl.Rule(honesty[ 'low' ] & cooperativeness[ 'low' ] & network_latency[ 'high' ], Trust[ 'low' ])
    rule26 = ctrl.Rule(honesty[ 'low' ] & cooperativeness[ 'low' ] & network_latency[ 'medium' ], Trust[ 'low' ])
    rule27 = ctrl.Rule(honesty[ 'low'] & cooperativeness[ 'low' ] & network_latency[ 'low' ], Trust[ 'low' ])

    Trust_ctrl1 = ctrl.ControlSystem([rule1, rule2, rule3, rule4 , rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20
                                     , rule21, rule22, rule23, rule24, rule25, rule26, rule27])
    #fog node                                 
    #define membership functions and rules of the trust model 
    availability = ctrl.Antecedent(np.arange(0, 1, 0.1), 'availability' )
    Response_time = ctrl.Antecedent(np.arange(0, 2001,1), 'response_time' )
    task_completion_rate = ctrl.Antecedent(np.arange(0, 1, 0.1), 'task_completion_rate' )
    Trust = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Trust' )

    availability[ 'low' ] = fuzz.trimf(availability.universe, [ 0, 0, 0.5])
    availability[ 'medium' ] = fuzz.trimf(availability.universe, [0, 0.5, 1])
    availability[ 'high' ] = fuzz.trimf(availability.universe, [ 0.5,1,1])

    Response_time[ 'low' ] = fuzz.trapmf(Response_time.universe, [ 0, 0, 100, 200])
    Response_time[ 'medium' ] = fuzz.trapmf(Response_time.universe, [ 100, 200,300, 400])
    Response_time[ 'high' ] = fuzz.trapmf(Response_time.universe, [ 300, 400, 2000, 2000])

    task_completion_rate[ 'low' ] = fuzz.trimf(task_completion_rate.universe, [ 0, 0, 0.5])
    task_completion_rate[ 'medium' ] = fuzz.trimf(task_completion_rate.universe, [0, 0.5, 1])
    task_completion_rate[ 'high' ] = fuzz.trimf(task_completion_rate.universe, [ 0.5,1,1])
    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    Trust[ 'low' ] = fuzz.trimf(Trust.universe, [ 0,0, 0.3])
    Trust[ 'medium' ] = fuzz.trimf(Trust.universe, [ 0.2, 0.5, 0.8])
    Trust[ 'high' ] = fuzz.trimf(Trust.universe, [ 0.7 ,1, 1 ])

    rule1 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'high' ] & task_completion_rate[ 'high' ], Trust[ 'high' ])
    rule2 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'high' ] & task_completion_rate[ 'medium' ] , Trust[ 'medium' ])
    rule3 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'high' ] & task_completion_rate[ 'low' ] , Trust[ 'low' ])

    rule4 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'medium' ] & task_completion_rate[ 'high' ] , Trust[ 'high'  ])
    rule5 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'medium' ] & task_completion_rate[ 'medium' ] , Trust[ 'medium' ])
    rule6 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'medium' ] & task_completion_rate[ 'low' ] , Trust[ 'medium'  ])

    rule7 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'low'  ] & task_completion_rate[ 'high' ] , Trust[ 'high' ])
    rule8 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'low'  ] & task_completion_rate[ 'medium' ] , Trust[ 'medium' ])
    rule9 = ctrl.Rule(availability[ 'high' ] & Response_time[ 'low'  ] & task_completion_rate[ 'low' ] , Trust[ 'low' ])

    rule10 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'high' ] & task_completion_rate[ 'high' ], Trust[ 'medium' ])
    rule11 = ctrl.Rule(availability[ 'medium'] & Response_time[ 'high' ] & task_completion_rate[ 'medium' ], Trust[ 'low'])
    rule12 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'high' ] & task_completion_rate[ 'low' ], Trust[ 'low' ])

    rule13 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'medium' ] & task_completion_rate[ 'high' ], Trust[ 'high'])
    rule14 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'medium' ] & task_completion_rate[ 'medium' ], Trust[ 'medium'  ])
    rule15 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'medium' ] & task_completion_rate[ 'low' ], Trust[ 'low'  ])

    rule16 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'low' ] & task_completion_rate[ 'high' ], Trust[ 'medium' ])
    rule17 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'low' ] & task_completion_rate[ 'medium' ], Trust[ 'medium' ])
    rule18 = ctrl.Rule(availability[ 'medium' ] & Response_time[ 'low' ] & task_completion_rate[ 'low' ], Trust[ 'medium' ])

    rule19 = ctrl.Rule(availability[ 'low' ] & Response_time[ 'high' ] & task_completion_rate[ 'high' ], Trust[ 'low' ])
    rule20 = ctrl.Rule(availability[ 'low'] & Response_time[ 'high' ] & task_completion_rate[ 'medium' ], Trust[ 'low' ])
    rule21 = ctrl.Rule(availability[ 'low' ] & Response_time[ 'high' ] & task_completion_rate[ 'low' ], Trust[ 'low' ])

    rule22 = ctrl.Rule(availability[ 'low' ] & Response_time[ 'medium' ] & task_completion_rate[ 'high' ], Trust[ 'medium' ])
    rule23 = ctrl.Rule(availability[ 'low' ] & Response_time[ 'medium' ] & task_completion_rate[ 'medium' ], Trust[ 'medium' ])
    rule24 = ctrl.Rule(availability[ 'low'] & Response_time[ 'medium' ] & task_completion_rate[ 'low' ], Trust[ 'low' ])

    rule25 = ctrl.Rule(availability[ 'low' ] & Response_time[ 'low' ] & task_completion_rate[ 'high' ], Trust[ 'high' ])
    rule26 = ctrl.Rule(availability[ 'low' ] & Response_time[ 'low' ] & task_completion_rate[ 'medium' ], Trust[ 'medium' ])
    rule27 = ctrl.Rule(availability[ 'low'] & Response_time[ 'low' ] & task_completion_rate[ 'low' ], Trust[ 'low' ])

    Trust_ctrl2 = ctrl.ControlSystem([rule1, rule2, rule3, rule4 , rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20
                                     , rule21, rule22, rule23, rule24, rule25, rule26, rule27])
    trustor=[]
    end_nodes=[]
    fog_nodes=[]
    
    endnode = int(arg1)
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
        t = threading.Timer(0.01, run,args=[trustor,end_nodes[p],evidence,"T1",Trust_ctrl1])
        t.start() 
        tasks.append(t)
    for p in range(0, fognode):
        t = threading.Timer(0.01, run,args=[trustor,fog_nodes[p],evidence2,"T2",Trust_ctrl2])
        t.start() 
        tasks.append(t)   
    for i in range(0, endnode+fognode):
        tasks[i].join()       
    #time.sleep(1)
    #measure resources
    subprocess.run(['sudo','sh', '/home/pi/aiocoap/smart_traffic/locally/cpu_usage_ps.sh'],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
if __name__ == "__main__":
    asyncio.run(main(sys.argv[1],sys.argv[2]))
