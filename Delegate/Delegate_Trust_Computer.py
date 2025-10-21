#!/usr/bin/env python3
from datetime import datetime
import threading
import multiprocessing
import logging
import json
import sqlite3
import asyncio
import uuid
import string
import statistics
import aiocoap.resource as resource
import aiocoap
import subprocess
import time
from E_collector import *
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from Update_Trust import Update_trust_weighted_sum, Update_trust_fuzzy_logic
from Check_Lease_Time import Check_Lease_Time

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"
class Delegate_Trust_Computer(resource.Resource): #used for POST /Trust_Computer
    def __init__(self):
        super().__init__()

    def Delegate_Trust_Computer_info(self, request, data):
        trustor = data["trustor"]
        trustee = data["trustee"]
        roles = ["TC"]
        roles = ','.join(roles)
        lease_time = data["lease_time"]
        t_model = data["t_model"]
        evidence= data["evidence"]
        share = data["share"]

        #convert data to database format
        evidence  = ','.join(data["evidence"])# specify evidence to store
        leasing_time = datetime.timestamp(datetime.now())+lease_time

        conn = sqlite3.connect(DB_Delegation)
        cursor_obj = conn.cursor()
        
        cursor_obj.execute("INSERT INTO Roles (role) VALUES (?)",(roles,))
        Role_id = cursor_obj.lastrowid
        conn.commit()

        conn.execute("INSERT INTO Delegation_info (trustor_ip, trustee_ip, Roles, lease_time, t_model, t_evidence, share) VALUES (?,?,?,?,?,?,?)",(trustor, trustee, Role_id, leasing_time, t_model, evidence, share))
        conn.commit()
        conn.close()
        print("\nStoring...Information Completed Trustor[...%s] and Trustee [...%s]"%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: Delegate_Trust_Computer from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))

        #Store delegation info
        for item in data:
            self.Delegate_Trust_Computer_info(request, item)

        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        
        print("\nStarting performing trust management on behalf of the delegators...")
        return aiocoap.Message(code=aiocoap.CREATED)

class Trust_Computer(resource.Resource): #used for POST /Trust_Computer
    def __init__(self):
        super().__init__()

    
    async def runweightedSum(self,data): 
        trustor_ip = data["trustor"]
        trustee_ip = data["trustee"]
        Old_trust_value = data["Old_trust_value"]
        response_time_list = data.get("response_time", [])
        distance_list = data.get("distance", [])
        packet_loss_rate_list = data.get("packet_loss_rate", [])
    
        # Handle empty lists 
        if not response_time_list:
            avg_response_time = 0
        else:
            avg_response_time = statistics.fmean(response_time_list)
        
        if not distance_list:
            avg_distance = 0
        else:
            avg_distance = statistics.fmean(distance_list)
        
        if not packet_loss_rate_list:
            avg_packet_loss_rate = 0
        else:
            avg_packet_loss_rate = statistics.fmean(packet_loss_rate_list)

        E_avg_value = {}
        E_avg_value["response_time"] = avg_response_time
        E_avg_value["distance"] = avg_distance
        E_avg_value["packet_loss_rate"] = avg_packet_loss_rate

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
        
        print('\n[TRUST COMPUTATION] Weighted Sum Update Trustor[...%s] and Trustee[...%s] VALUE = %s '%(str(trustor_ip.split(':', 4)[4]),str(trustee_ip.split(':', 4)[4]),Trust_value))
        return Trust_value
    
    async def runfuzzy(self,data,final_Trust):
    
        trustor_ip = data["trustor"]
        trustee_ip = data["trustee"]
        Old_trust_value = data["Old_trust_value"]

        response_time_list = data.get("response_time", [])
        distance_list = data.get("distance", [])
        packet_loss_rate_list = data.get("packet_loss_rate", [])
    
        # Handle empty lists safely
        if not response_time_list:
            avg_response_time = 0
        else:
            avg_response_time = statistics.fmean(response_time_list)
        
        if not distance_list:
            avg_distance = 0
        else:
            avg_distance = statistics.fmean(distance_list)
        
        if not packet_loss_rate_list:
            avg_packet_loss_rate = 0
        else:
            avg_packet_loss_rate = statistics.fmean(packet_loss_rate_list)

        E_avg_value = {}
        E_avg_value["response_time"] = avg_response_time
        E_avg_value["distance"] = avg_distance
        E_avg_value["packet_loss_rate"] = avg_packet_loss_rate
       
        #compute a trust value by fuzzy logic 
        final_Trust.input[ 'Distance' ] = E_avg_value["distance"]
        final_Trust.input[ 'Response_time' ] = E_avg_value["response_time"] 
        final_Trust.input[ 'packet_loss_rate' ] = E_avg_value["packet_loss_rate"]
        # Crunch the numbers
        final_Trust.compute()
        # final_trust.compute_rule(rules)
        Trust_value = final_Trust.output[ 'Trust' ]
        Trust_value= str(f'{Trust_value:.2f}')
        #print('[%s][...%s] Trust value = %s '%(i,str(trustee_ip.split(':', 4)[4]),Trust_value))

        print('\n[TRUST COMPUTATION] Fuzzy-logic Update Trustor[...%s] and Trustee[...%s] VALUE = %s '%(str(trustor_ip.split(':', 4)[4]),str(trustee_ip.split(':', 4)[4]),Trust_value))
        return Trust_value


    async def Trust_Computer(self, data):
        trustor = data["trustor"]
        trustee = data["trustee"]
        conn = sqlite3.connect(DB_Delegation)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "select * from Delegation_info where trustor_ip = ? AND trustee_ip = ?"
        cur.execute(sql, (trustor, trustee))
        row = cur.fetchone()
        if row: 
            T_model = row["T_model"]
        conn.close()
        #---------------
        #define membership functions and rules of the trust model 
        if T_model == "fuzzy-logic":
            Distance = ctrl.Antecedent(np.arange(0, 5, 1), 'Distance' )
            Response_time = ctrl.Antecedent(np.arange(0, 2001,1), 'Response_time' )
            packet_loss_rate = ctrl.Antecedent(np.arange(0, 11, 1), 'packet_loss_rate' )
            Trust = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Trust' )

            Distance[ 'low' ] = fuzz.trimf(Distance.universe, [ 0, 0, 2])
            Distance[ 'medium' ] = fuzz.trimf(Distance.universe, [1, 2, 3])
            Distance[ 'high' ] = fuzz.trimf(Distance.universe, [ 2,4,4])

            Response_time[ 'low' ] = fuzz.trapmf(Response_time.universe, [ 0, 0, 100, 200])
            Response_time[ 'medium' ] = fuzz.trapmf(Response_time.universe, [ 100, 200,300, 400])
            Response_time[ 'high' ] = fuzz.trapmf(Response_time.universe, [ 300, 400, 2000, 2000])

            packet_loss_rate[ 'low' ] = fuzz.trapmf(packet_loss_rate.universe, [ 0, 0, 2, 3])
            packet_loss_rate[ 'medium' ] = fuzz.trapmf(packet_loss_rate.universe, [2,3, 4, 5])
            packet_loss_rate[ 'high' ] = fuzz.trapmf(packet_loss_rate.universe, [ 4, 5 ,10,10])
            # Custom membership functions can be built interactively with a familiar,
            # Pythonic API
            Trust[ 'low' ] = fuzz.trimf(Trust.universe, [ 0,0, 0.3])
            Trust[ 'medium' ] = fuzz.trimf(Trust.universe, [ 0.2, 0.5, 0.8])
            Trust[ 'high' ] = fuzz.trimf(Trust.universe, [ 0.7 ,1, 1 ])

            rule1 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'high' ] & packet_loss_rate[ 'high' ], Trust[ 'low' ])
            rule2 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'high' ] & packet_loss_rate[ 'medium' ] , Trust[ 'low' ])
            rule3 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'high' ] & packet_loss_rate[ 'low' ] , Trust[ 'low' ])

            rule4 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'high' ] , Trust[ 'low'  ])
            rule5 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'medium' ] , Trust[ 'medium' ])
            rule6 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'low' ] , Trust[ 'medium'  ])

            rule7 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'low'  ] & packet_loss_rate[ 'high' ] , Trust[ 'low' ])
            rule8 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'low'  ] & packet_loss_rate[ 'medium' ] , Trust[ 'medium' ])
            rule9 = ctrl.Rule(Distance[ 'high' ] & Response_time[ 'low'  ] & packet_loss_rate[ 'low' ] , Trust[ 'high' ])

            rule10 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'high' ] & packet_loss_rate[ 'high' ], Trust[ 'low' ])
            rule11 = ctrl.Rule(Distance[ 'medium'] & Response_time[ 'high' ] & packet_loss_rate[ 'medium' ], Trust[ 'low'])
            rule12 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'high' ] & packet_loss_rate[ 'low' ], Trust[ 'medium' ])

            rule13 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'high' ], Trust[ 'low'])
            rule14 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'medium' ], Trust[ 'medium'  ])
            rule15 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'low' ], Trust[ 'high'  ])

            rule16 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'low' ] & packet_loss_rate[ 'high' ], Trust[ 'medium' ])
            rule17 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'low' ] & packet_loss_rate[ 'medium' ], Trust[ 'high' ])
            rule18 = ctrl.Rule(Distance[ 'medium' ] & Response_time[ 'low' ] & packet_loss_rate[ 'low' ], Trust[ 'high' ])

            rule19 = ctrl.Rule(Distance[ 'low' ] & Response_time[ 'high' ] & packet_loss_rate[ 'high' ], Trust[ 'low' ])
            rule20 = ctrl.Rule(Distance[ 'low'] & Response_time[ 'high' ] & packet_loss_rate[ 'medium' ], Trust[ 'medium' ])
            rule21 = ctrl.Rule(Distance[ 'low' ] & Response_time[ 'high' ] & packet_loss_rate[ 'low' ], Trust[ 'high' ])

            rule22 = ctrl.Rule(Distance[ 'low' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'high' ], Trust[ 'medium' ])
            rule23 = ctrl.Rule(Distance[ 'low' ] & Response_time[ 'medium' ] & packet_loss_rate[ 'medium' ], Trust[ 'medium' ])
            rule24 = ctrl.Rule(Distance[ 'low'] & Response_time[ 'medium' ] & packet_loss_rate[ 'low' ], Trust[ 'high' ])

            rule25 = ctrl.Rule(Distance[ 'low' ] & Response_time[ 'low' ] & packet_loss_rate[ 'high' ], Trust[ 'high' ])
            rule26 = ctrl.Rule(Distance[ 'low' ] & Response_time[ 'low' ] & packet_loss_rate[ 'medium' ], Trust[ 'high' ])
            rule27 = ctrl.Rule(Distance[ 'low'] & Response_time[ 'low' ] & packet_loss_rate[ 'low' ], Trust[ 'high' ])

            Trust_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4 , rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20
                                            , rule21, rule22, rule23, rule24, rule25, rule26, rule27])
            final_Trust = ctrl.ControlSystemSimulation(Trust_ctrl)

        # Check lease time
        expiry = check_lease_time(trustor, trustee)
        if expiry:
            print(f'\n[TRUST COMPUTATION] Delegation expired')
            return "Delegation lease time has expired"
        
        # Run trust computation
        if T_model == "weighted sum":
            trust_value = await self.runweightedSum(data)
        elif T_model == "fuzzy-logic":
            trust_value = await self.runfuzzy(data, final_Trust)

        return trust_value

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: Trust_Computer from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))
        trust_value = await self.Trust_Computer(data)
        payload = {"trust_value": trust_value}
        payload = json.dumps(payload)
        payload = payload.encode('ascii')
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        return aiocoap.Message(payload = payload)
        