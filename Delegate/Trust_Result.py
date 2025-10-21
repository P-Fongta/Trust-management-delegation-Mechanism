#!/usr/bin/env python3

import json
import sqlite3
import aiocoap.resource as resource
import aiocoap

# Database path
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"

class Trust_Result(resource.Resource):
    def __init__(self):
        super().__init__()

    def Get_trust(self,data):
        trustor_ip = data["trustor"]
        trustee_ip = data["trustee"]
        threshold = data["threshold"]

        if threshold != "":
            conn = sqlite3.connect(DB_Trust_value)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql = "select * from Trust_value where trustor_ip = ? AND trustee_ip = ?"
            cur.execute(sql,(trustor_ip,trustee_ip))
            row = cur.fetchone()
            if row: 
                trust_value= row["trust_value"]
            conn.close()    

            # model for decision making
            if trust_value >= threshold:
                trust_result = "trusted"
            else:
                trust_result = "untrusted"  
            #print('Trust value =  %s (%s)'%(trust_value, trust_result )) 
            print('\n[TD Decision Making] Trustor[...%s] and Trustee[...%s] VALUE = %s '%(str(trustor_ip.split(':', 4)[4]),str(trustee_ip.split(':', 4)[4]), trust_result))
            trust_result = {"trust": trust_result}
        elif threshold == "":
            conn = sqlite3.connect(DB_Trust_value)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql = "SELECT trustee_ip, trust_value FROM trust_value WHERE trustor_ip = ? ORDER BY trust_value DESC LIMIT 1"
            cur.execute(sql,(trustor_ip,))
            row = cur.fetchone() 
            if row:
                highest_trustee = row["trustee_ip"]
                highest_value = row["trust_value"]
                #print(f"Highest Trust value: {highest_trustee} = {highest_value}")

            
            #print('Trust value =  %s (%s)'%(trust_value, trust_result )) 
            print('\n[TBD Decision Making] Highest Trustee: [%s] Value %s '%(highest_trustee, highest_value))
            trust_result = {"highest_trustee": highest_trustee,"highest_value": highest_value }

        return trust_result

    async def render_get(self, request):
        print("\nRecv: Trust_Result from [...%s]"%(str(request.unresolved_remote.split(':', 4)[4]))) 
        data = json.loads(request.payload)
        payload = self.Get_trust(data)
        print("\nResp: to [...%s]"%(str(request.unresolved_remote.split(':', 4)[4])))  
        payload = json.dumps(payload)
        payload = payload.encode('ascii')
        #print("\nResp: to {}".format(request.unresolved_remote))
        return aiocoap.Message(payload=payload)