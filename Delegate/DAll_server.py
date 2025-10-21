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

from Delegate_All_Roles import Delegate_All_Roles
from Delegate_Trust_Computer_Repositor import Delegate_Trust_Computer_Repositor
from Delegate_Trust_Repositor import Delegate_Trust_Repositor
from Delegate_Evidence_Collector import Delegate_Evidence_Collector
from Delegate_Trust_Computer import Delegate_Trust_Computer, Trust_Computer
from Evidence_Storage import Evidence_Storage
from Trust_Value_Storage import Trust_Value_Storage
from Trust_Result import Trust_Result
from Trust_Evidence import Trust_Evidence
from Trust_Value import Trust_Value
from Access_control import Grant_Permission, Revoke_Permission
from Handover import Handover_Request, Delegation_Info_Request

DB_Delegation = "/home/pi/aiocoap/DB/Delegation.db"
DB_Trust_value = "/home/pi/aiocoap/DB/Trust_value.db"
DB_Trust_evidence = "/home/pi/aiocoap/DB/Trust_evidence.db"

# logging setup
#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    print("Waiting for connection...")
    global root
    root = resource.Site()

    root.add_resource(['Delegate_All_Roles'], Delegate_All_Roles())
    root.add_resource(['Delegate_Trust_Computer_Repositor'], Delegate_Trust_Computer_Repositor())
    root.add_resource(['Delegate_Evidence_Collector'], Delegate_Evidence_Collector())
    root.add_resource(['Delegate_Trust_Repositor'], Delegate_Trust_Repositor())
    root.add_resource(['Delegate_Trust_Computer'], Delegate_Trust_Computer())
    root.add_resource(['Trust_Computer'], Trust_Computer())
    root.add_resource(['Evidence_Storage'], Evidence_Storage())
    root.add_resource(['Trust_Value_Storage'], Trust_Value_Storage())
    root.add_resource(['Trust_Result'], Trust_Result())
    root.add_resource(['Trust_Evidence'], Trust_Evidence())
    root.add_resource(['Trust_Value'], Trust_Value())
    root.add_resource(['Grant_Permission'], Grant_Permission())
    root.add_resource(['Revoke_Permission'], Revoke_Permission())
    root.add_resource(['Handover_Request'], Handover_Request())
    root.add_resource(['Delegation_Info_Request'], Delegation_Info_Request())
    

    await aiocoap.Context.create_server_context(root)
    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
