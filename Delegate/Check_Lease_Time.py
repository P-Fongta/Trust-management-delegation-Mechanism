#!/usr/bin/env python3

import json
import sqlite3
import aiocoap.resource as resource
import aiocoap
import time
from datetime import datetime


# Database path
DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"

def Check_Lease_Time(trustor,trustee):
    conn = sqlite3.connect(DB_Delegation)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = "select * from Delegation_info where trustor_ip = %s AND trustee_ip = %s" %(repr(trustor), repr(trustee))
    cur.execute(sql)
    row = cur.fetchone()
    leasing_time = row["Lease_time"]
    conn.close() 
    if datetime.now().timestamp() > float(leasing_time):
        #print("\n[Delegation] Delegation END Trustor[...%s] and Trustee [...%s]"%(str(trustor.split(':', 4)[4]),str(trustee.split(':', 4)[4])))
        return 1
    else:
        return 0 