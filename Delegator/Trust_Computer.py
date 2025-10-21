#!/usr/bin/env python3


from datetime import datetime
import logging
import asyncio
import json
import subprocess
from aiocoap import *
from E_collector import *

# logging setup
#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)

DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"


async def Trust_Computer(protocol, delegator_IP, data, Old_trust_value):
    trustor_ip = data["trustor"]
    trustee_ip = data["trustee"]
    all_evidence = data["evidence"]
    Evidence_list=[]
    E_dict = {}
    E_dict["trustor"] = trustor_ip
    E_dict["trustee"] = trustee_ip
    E_dict["Old_trust_value"] = Old_trust_value

    conn = sqlite3.connect(DB_Trust_evidence)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    for p in all_evidence:
        sql = f"select Evidence_id, Evidence_value from Trust_evidence where Evidence_name = ? and trustor_ip = ? and trustee_ip = ? ORDER BY timestamp"
        cur.execute(sql, (p,trustor_ip,trustee_ip))
        new_entries = cur.fetchall()
        conn.commit()
        for row in new_entries:
            rowid = row[0]
            evidence_value = row[1]
            Evidence_list.append(evidence_value)
        E_dict[p]=Evidence_list.copy()
        Evidence_list=[]

    conn.close()
    y = json.dumps(E_dict)
    payload = y.encode('ascii')
    print("\nSending: Trust_Computer to [...%s]"%(str(delegator_IP.split(':', 4)[4])))

    protocol = await Context.create_client_context()
    request = Message(code=POST, payload=payload, uri=f'coap://[{delegator_IP}]/Trust_Computer')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    trust_result = json.loads(response.payload)
    print('Recv: from [...%s] Trust Value of [...%s] = %s'%(str(response.unresolved_remote.split(':', 4)[4]), str(trustee_ip.split(':', 4)[4]), trust_result["trust_value"] ))
