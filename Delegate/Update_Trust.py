#!/usr/bin/env python3

from datetime import datetime
import sqlite3
import statistics

DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

async def Query_evidence(trustor_ip,trustee_ip):
    E_dict = {}
    E_avg_value = {}
    #print('[Trust Update] Update trust Trustor[...%s] and Trustee[...%s] '%(str(trustor_ip.split(':', 4)[4]),str(trustee_ip.split(':', 4)[4])))
    conn = sqlite3.connect(DB_Delegation)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = "select * from Delegation_info where trustor_ip = ? AND trustee_ip = ?"
    cur.execute(sql,(trustor_ip,trustee_ip))
    row = cur.fetchone()
    if row: 
        evidence_list= row["T_evidence"]
    conn.close()
    evidence_list = evidence_list.split(",")
    conn = sqlite3.connect(DB_Trust_evidence)
    for p in evidence_list:
        if p == "response_time":
            Response_time_list=[]
            #print('Querying %s'%(p))
            sql1 = "select Evidence_value from Trust_evidence where Evidence_name = %s and trustor_ip = %s AND trustee_ip = %s and timestamp >= datetime(CURRENT_TIMESTAMP,'-100 hours')" %(repr(p),repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql1):
                Response_time_list.append(row[0])
                
            if len(Response_time_list) == 0:
                avg_response_time=0
            else:
                avg_response_time = statistics.fmean(Response_time_list)
            E_avg_value[p] = avg_response_time 
            E_dict[p]=Response_time_list
        elif p == "distance":
            #print('Querying %s'%(p))
            distance_list=[]
            sql2 = "select Evidence_value from Trust_evidence where Evidence_name = %s and trustor_ip = %s AND trustee_ip = %s and timestamp >= datetime(CURRENT_TIMESTAMP,'-100 hours')" %(repr(p), repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                distance_list.append(row[0])
            
            if len(distance_list) == 0:
                avg_distance=0
            else:
                avg_distance = statistics.fmean(distance_list)
            E_avg_value[p] = avg_distance 
            E_dict[p]=distance_list
        elif p == "packet_loss_rate":
            #print('Querying %s'%(p))
            packet_loss_rate_list=[]
            sql2 = "select Evidence_value from Trust_evidence where Evidence_name = %s and trustor_ip = %s AND trustee_ip = %s and timestamp >= datetime(CURRENT_TIMESTAMP,'-100 hours')" %(repr(p),repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                packet_loss_rate_list.append(row[0])
            
            if len(packet_loss_rate_list) == 0:
                avg_packet_loss_rate=0
            else:
                avg_packet_loss_rate = statistics.fmean(packet_loss_rate_list)
            E_avg_value[p] = avg_packet_loss_rate
            E_dict[p]=packet_loss_rate_list
        elif p == "availability":
            #print('Querying %s'%(p))
            availability_list=[]
            sql2 = "select Evidence_value from Trust_evidence where Evidence_name = %s and trustor_ip = %s AND trustee_ip = %s and timestamp >= datetime(CURRENT_TIMESTAMP,'-100 hours')" %(repr(p),repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                availability_list.append(row[0])
            
            if len(availability_list) == 0:
                avg_availability=0
            else:
                avg_availability = statistics.fmean(availability_list)
            E_avg_value[p] = avg_availability
            E_dict[p]=availability_list
        elif p == "task_completion_rate":
            #print('Querying %s'%(p))
            task_completion_rate_list=[]
            sql2 = "select Evidence_value from Trust_evidence where Evidence_name = %s and trustor_ip = %s AND trustee_ip = %s and timestamp >= datetime(CURRENT_TIMESTAMP,'-100 hours')" %(repr(p),repr(trustor_ip), repr(trustee_ip))
            for row in conn.execute(sql2):
                task_completion_rate_list.append(row[0])
            
            if len(task_completion_rate_list) == 0:
                avg_task_completion_rate=0
            else:
                avg_task_completion_rate = statistics.fmean(task_completion_rate_list)
            E_avg_value[p] = avg_task_completion_rate
            E_dict[p]=task_completion_rate_list
    conn.close()
    return(E_avg_value)

async def Update_trust_weighted_sum(trustor_ip,trustee_ip):
        E_avg_value = {}
        E_avg_value= await Query_evidence(trustor_ip,trustee_ip)
        #print(E_dict)   
        
        #measure resources
        #subprocess.run(['sudo', 'sh', 'cpu_usage_ps.sh', 'python', 'delegation_server1.txt'],stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        #Trust model
        Score_Response_time =1
        Score_distance =1
        Score_packet_loss_rate = 1
        
        if E_avg_value["response_time"] < 150: 
            Score_Response_time = 1
        elif E_avg_value["response_time"] > 151 and E_avg_value["response_time"] < 400 :
            Score_Response_time = 0.5
        elif E_avg_value["response_time"] >= 400 :
            Score_Response_time = 0
            
        if E_avg_value["distance"] == 0:
            Score_distance = 1
        elif E_avg_value["distance"] == 1:
            Score_distance = 0.5
        elif E_avg_value["distance"] >= 2 :
            Score_distance = 0
            
        if E_avg_value["packet_loss_rate"] < 2:
            Score_packet_loss_rate = 1
        elif E_avg_value["packet_loss_rate"] >= 2 and E_avg_value["packet_loss_rate"] <= 5 :
            Score_packet_loss_rate = 0.5
        elif E_avg_value["packet_loss_rate"] > 5 :
            Score_packet_loss_rate = 0
        W1 = 1/3
        W2 = 1/3
        W3 = 1/3
        Trust_value = ((W1*Score_Response_time)+(W2*Score_distance)+(W3*Score_packet_loss_rate))
        Trust_value= str(f'{Trust_value:.2f}')
        #print('[%s][...%s] Trust value = %s '%(i,str(trustee_ip.split(':', 4)[4]),Trust_value))
        
        #update trust value in database
        conn = sqlite3.connect(DB_Trust_value)
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
        
        print('\n[Trust Update] Update trust Trustor[...%s] and Trustee[...%s] VALUE = %s '%(str(trustor_ip.split(':', 4)[4]),str(trustee_ip.split(':', 4)[4]),Trust_value))
async def Update_trust_fuzzy_logic(trustor_ip,trustee_ip,final_Trust):
        E_avg_value = {}
        E_avg_value= await Query_evidence(trustor_ip,trustee_ip)

        #compute a trust value by fuzzy logic 
        final_Trust.input[ 'Distance' ] = E_avg_value["avg_distance"]
        final_Trust.input[ 'Response_time' ] = E_avg_value["avg_response_time"] 
        final_Trust.input[ 'packet_loss_rate' ] = E_avg_value["avg_packet_loss_rate"]
        # Crunch the numbers
        final_Trust.compute()
        # final_trust.compute_rule(rules)
        Trust_value = final_Trust.output[ 'Trust' ]
        Trust_value= str(f'{Trust_value:.2f}')
        #print('[%s][...%s] Trust value = %s '%(i,str(trustee_ip.split(':', 4)[4]),Trust_value))
        
        #update trust value in database
        conn = sqlite3.connect('/home/pi/aiocoap/e-health/DB/trust.db')
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
        
        print('\n[Trust Update] fuzzy Update trust Trustor[...%s] and Trustee[...%s] VALUE = %s '%(str(trustor_ip.split(':', 4)[4]),str(trustee_ip.split(':', 4)[4]),Trust_value))
            