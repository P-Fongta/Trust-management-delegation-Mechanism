#!/usr/bin/env python3

import json
import sqlite3
import aiocoap.resource as resource
import aiocoap

# Database path
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

class Evidence_Storage(resource.Resource): #used for POST /Evidence_Storage
    def __init__(self):
        super().__init__()


    async def E_storage(self,data):
        trustor = data["trustor"]
        trustee = data["trustee"]

        conn = sqlite3.connect(DB_Trust_evidence)
        for key_name, key_value in data.items():
            if key_name in ["trustor", "trustee"]:
                continue
            if isinstance(key_value, (list, tuple)):
                values = key_value
            else:
                values = [key_value]  # Convert single value to list

            for value in values:
                conn.execute(
                        "INSERT INTO Trust_evidence (trustor_ip, trustee_ip, Evidence_name, Evidence_value) VALUES (?,?,?,?)",
                        (trustor, trustee, key_name, value)
                    )
        conn.commit()
        conn.close()
        print('\n[EVIDENCE_STORAGE] Completed Trustor[...%s] and Trustee [...%s]'%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))
        

    async def render_post(self, request):
        data = json.loads(request.payload)
        print('\nRecv: EVIDENCE_STORAGE from [...%s] '%(str(request.unresolved_remote.split(':', 4)[4])))
        await self.E_storage(data)  
        print('\nResp: to %s'%(str(request.unresolved_remote.split(':', 4)[4])))
        return aiocoap.Message(code=aiocoap.CREATED)
    
     