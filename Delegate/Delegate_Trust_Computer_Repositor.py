from datetime import datetime
import json
import sqlite3
import asyncio
import aiocoap.resource as resource
import aiocoap
import time
from E_collector import *
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Import the standalone functions
from Update_Trust import Update_trust_weighted_sum, Update_trust_fuzzy_logic

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"

class Delegate_Trust_Computer_Repositor(resource.Resource):
    def __init__(self):
        super().__init__()

    def Delegate_Trust_Computer_Repositor_info(self, data):
        trustor = data["trustor"]
        trustee = data["trustee"]
        roles = ["TC","TR"]
        roles = ','.join(roles)
        lease_time = data["lease_time"]
        t_model = data["t_model"]
        t_update = data["t_update"]
        evidence= data["evidence"]
        share = data["share"]

        #convert data to database format
        evidence  = ','.join(data["evidence"])# specify evidence to store
        Evidence_collect = ','.join(data["evidence"])# specify evidence to collect
        Evidence_store  = ','.join(data["evidence"])# specify evidence to store
        leasing_time = datetime.timestamp(datetime.now())+lease_time
        print("\nStoring...Delegation Information Trustor[...%s] and Trustee[...%s]  "%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))

        conn = sqlite3.connect(DB_Delegation)
        cursor_obj = conn.cursor()
        
        cursor_obj.execute("INSERT INTO Roles (role) VALUES (?)",(roles,))
        Role_id = cursor_obj.lastrowid
        conn.commit()

        cursor_obj.execute("INSERT INTO E_collector (Evidence) VALUES (?)",(Evidence_collect,))
        Ecollector_id = cursor_obj.lastrowid
        conn.commit()

        cursor_obj.execute("INSERT INTO E_storage (Evidence) VALUES (?)",(Evidence_store,))
        Estorage_id = cursor_obj.lastrowid
        conn.commit()
         
        conn.execute("INSERT INTO Delegation_info (trustor_ip, trustee_ip, Roles, lease_time, t_model, t_update, E_storage, E_collector, t_evidence, share) VALUES (?,?,?,?,?,?,?,?,?,?)",(trustor, trustee, Role_id, leasing_time, t_model, t_update, Estorage_id, Ecollector_id, evidence, share))
        conn.commit()
        conn.close()
        conn1 = sqlite3.connect(DB_Trust_value) # assign trust value =0.5
        conn1.execute("INSERT INTO trust_value (trustor_ip, trustee_ip,trust_value) VALUES (?,?,?)",(trustor, trustee,"0.5"))
        conn1.commit()
        conn1.close() 

        print("\nStoring...Information Completed Trustor[...%s] and Trustee [...%s]"%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))
        
        #print("\n[Delegation] Sending Delegation Result to [...%s] DONE "%(str(trustor.split(':', 4)[4])))
    
    async def runweightedSum(self,data): 
    
        trustor = data["trustor"]
        trustee = data["trustee"]
        #tasks = [Update_trust(trustor, trustee),response_time(IP), availability(IP), task_completion_rate(IP)  ]

        tasks = [Update_trust_weighted_sum(trustor, trustee)]
        await asyncio.gather(*tasks)
    
    async def runfuzzy(self,i,data,final_Trust):
    
        trustor = data["trustor"]
        trustee = data["trustee"]
        
        Update_trust_fuzzy_logic(trustor, trustee,final_Trust)
         
        
    async def Delegate_Trust_Computer_Repositor(self,data):
        
        trustor = data["trustor"]
        trustee = data["trustee"]
        conn = sqlite3.connect(DB_Delegation)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "select * from Delegation_info where trustor_ip = ? AND trustee_ip = ?"
        cur.execute(sql, (trustor, trustee))
        row = cur.fetchone()
        if row: 
            T_update = row["T_update"]
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
            #--------------------------
        if T_update == "time-driven":
            measurement_count = 0
            # Define frequency intervals
            TRUST_UPDATE_FREQ = 3600 # Every 600th iteration (1hr)
            while True:
                
                # Run trust update
                if T_model == "weighted sum":
                    await self.runweightedSum(data)
                elif T_model == "fuzzy-logic":
                    await self.runfuzzy(data, final_Trust)
                print('\n[Time-Driven Update] Completed - Next update in 1 hour - Trustor[...%s] and Trustee[...%s]'%(str(trustor.split(':', 4)[4]), str(trustee.split(':', 4)[4])))

                # Check lease time
                expiry = check_lease_time(trustor, trustee)
                if expiry:
                    print(f'\n[Time-Driven Update] Delegation expired')
                    break
                
                measurement_count += 1
                # Reset counter to prevent overflow (optional)
                if measurement_count >= 36000:  # Reset after 10 hours
                    measurement_count = 0
                # Sleep for 1 m
                await asyncio.sleep(TRUST_UPDATE_FREQ) 

        elif T_update == "event-driven":
            i=0 
            last_checked_time = ""
            while True:
                # check new data is inserted
                conn = sqlite3.connect(DB_Trust_evidence)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                sql = "SELECT DISTINCT trustor_ip, trustee_ip, Evidence_name, timestamp FROM Trust_evidence WHERE timestamp > ? ORDER BY timestamp DESC"
                cur.execute(sql, (last_checked_time,))
                new_entries = cur.fetchall()
                conn.close()
                if new_entries:
                    # Run trust update
                    if T_model == "weighted sum":
                        await self.runweightedSum(data)
                    elif T_model == "fuzzy-logic":
                        await self.runfuzzy(data, final_Trust)
                    print('\n[Event-Driven Update] Completed - Trustor[...%s] and Trustee[...%s]'%(str(trustor.split(':', 4)[4]), str(trustee.split(':', 4)[4])))
                # Check lease time
                expiry = check_lease_time(trustor, trustee)
                # in experiments, we run just only 10 times instead of until lease time expires
                """ 
                if expiry:
                    print(f'\n[Time-Driven Update] Delegation expired')
                    break
                """ 
                i=i+1
                time.sleep(1)

    async def render_post(self, request):
        data = json.loads(request.payload)
        print("\nRecv: Delegate_Trust_Computer_Repositor from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 

        #Store delegation info
        for item in data:
            self.Delegate_Trust_Computer_Repositor_info(item) 
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        print("\nStarting performing trust management on behalf of the delegators...")
        
        tasks = []
        for item in data:
            asyncio.create_task(self.Delegate_Trust_Computer_Repositor(item)) 
        
        return aiocoap.Message(code=aiocoap.CREATED)