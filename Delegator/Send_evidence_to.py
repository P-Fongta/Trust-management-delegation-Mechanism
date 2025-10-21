#!/usr/bin/env python3


from datetime import datetime
import logging
import asyncio
import json
import subprocess
from aiocoap import *

async def Send_evidence_to(protocol, delegator_IP, data, sending_time):
    trustor = data["trustor"]
    trustee = data["trustee"]
    all_evidence = data["evidence"]
    Evidence_list=[]
    E_dict = {}
    for info in ["trustor", "trustee"]:
        E_dict[info] = eval(info)
    conn = sqlite3.connect(DB_Trust_evidence)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    for p in all_evidence:
        if sending_time == "Period Send": #  Period Send or Immediate Send
            sql = f"select Evidence_id, Evidence_value from Trust_evidence where Evidence_name = ? and trustor_ip = ? and trustee_ip = ? ORDER BY timestamp"
            cur.execute(sql, (p,trustor,trustee))
            new_entries = cur.fetchall()
            conn.commit()
            for row in new_entries:
                rowid = row[0]
                evidence_value = row[1]
                Evidence_list.append(evidence_value)
                #print(Evidence_list)
                sql2 = "DELETE FROM Trust_evidence WHERE Evidence_id = ?"
                cur.execute(sql2, (rowid,))
                conn.commit()
            E_dict[p]=Evidence_list.copy()
            Evidence_list=[]
        elif sending_time == "Immediate Send": #  Period Send or Immediate Send
            sql = f"select Evidence_id, Evidence_value from Trust_evidence where Evidence_name = ? and trustor_ip = ? and trustee_ip = ? ORDER BY timestamp DESC LIMIT 1"
            cur.execute(sql, (p,trustor,trustee))
            new_entries = cur.fetchall()
            conn.commit()
            for row in new_entries:
                rowid = row[0]
                evidence_value = row[1]
                Evidence_list.append(evidence_value)
                #print(Evidence_list)
                sql2 = "DELETE FROM Trust_evidence WHERE Evidence_id = ?"
                cur.execute(sql2, (rowid,))
                conn.commit()
            E_dict[p]=Evidence_list.copy()
            Evidence_list=[]
    conn.close()
    y = json.dumps(E_dict)
    payload = y.encode('ascii')
    print("\nSending: Evidence_Storage to [...%s]"%(str(delegator_IP.split(':', 4)[4])))

    protocol = await Context.create_client_context()
    request = Message(code=POST, payload=payload, uri=f'coap://[{delegator_IP}]/Evidence_Storage')
    #print('Payload: %s'%(payload))
    response = await protocol.request(request).response
    print('Recv: from [...%s] Result: %s'%(str(response.unresolved_remote.split(':', 4)[4]), response.code))
