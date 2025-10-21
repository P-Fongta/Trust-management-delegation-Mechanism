
"""Service Discovery for TSS"""

from datetime import datetime
import logging
import json
import sqlite3
import asyncio
import uuid
import time
import aiocoap.resource as resource
import aiocoap
# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

DB_name = "/home/pi/aiocoap/DB/Delegation_Registration.db"

class Register(resource.Resource):
    def __init__(self):
        super().__init__()

    def into_DB(self,ip, lease_time, roles, t_model, e_storage, e_collector, d_maker ):
        
        conn = sqlite3.connect(DB_name)
        conn.execute("INSERT INTO Service_Registration (Delegate_ip,Lease_time)  VALUES (?,?)",( ip, lease_time))
        conn.commit()
        cursor_obj = conn.cursor()
        sql = "select Reg_id from Service_Registration where Delegate_ip  = ? "
        cursor_obj.execute(sql, (ip,))
        ref = cursor_obj.fetchone()
        ref = ref[0]
        #print(ref)
        conn.commit()
        for x in roles:
            conn.execute("INSERT INTO roles (Role_id ,role)  VALUES (?,?)",(ref, x))
            conn.commit()
        for x in t_model:
            conn.execute("INSERT INTO trust_model (TModel_id,Trust_model)  VALUES (?,?)",(ref, x))
            conn.commit()
        for x in e_storage:
            conn.execute("INSERT INTO E_storage(Estorage_id,evidence)  VALUES (?,?)",(ref, x))
            conn.commit()
        for x in e_collector:
            conn.execute("INSERT INTO E_collector(Ecollector_id,Evidence)  VALUES (?,?)",(ref, x))
            conn.commit()
        for x in d_maker:
            conn.execute("INSERT INTO Decision_making_method(DMaking_id,Decision_making)  VALUES (?,?)",(ref, x))
            conn.commit()
        
        conn.close() 
        return ref

    async def render_post(self, request):
        print("\nRecv: REG_Request from {}".format(request.unresolved_remote))
        print("{}\n".format(request))
        data = json.loads(request.payload)
        #print(json.dumps(data))
        conn = sqlite3.connect(DB_name)
        cursor_obj = conn.cursor()
        sql = "select COUNT(*) from Service_Registration where Delegate_ip  = ?"
        cursor_obj.execute(sql, (data['ip'],))
        count = cursor_obj.fetchone()[0]
        if count > 0:
            payload = f'Delegate IP {data["ip"]} has already been registered'.encode('ascii')
            return aiocoap.Message(code=aiocoap.CREATED, payload=payload)
        else:
            leasing_time = datetime.timestamp(datetime.now())+data['lease_time']
            Ref = self.into_DB(data['ip'], leasing_time, data['roles'], data['t_model'], data['e_storage'], data['e_collector'], data['d_maker'])   
            payload = str(Ref).encode('ascii')
            print('Registration Completed...\nIP:  %s\nREG ref: %s\nRegistration expiry: %s'%(data['ip'], payload.decode('UTF-8'), datetime.fromtimestamp(int(leasing_time))))
            print("\nResp: to {}".format(request.unresolved_remote))
            return aiocoap.Message(code=aiocoap.CREATED, payload=payload)
       
        
class DeRegister(resource.Resource):
    def __init__(self):
        super().__init__()

    def Del_DB(self,ref,roles):
        
        conn = sqlite3.connect(DB_name)
        print('Registration Ref: %s'%(ref))
        for x in roles:
            print('Deregister role: %s'%(x))
            conn.execute("DELETE FROM roles WHERE Role_id = ? and role = ?;",(ref, x))
            conn.commit()
            if "TC" == x:
                conn.execute("DELETE FROM trust_model WHERE TModel_id = ?;",(ref,))
                conn.commit()
            elif "TR" == x:
                conn.execute("DELETE FROM E_storage WHERE Estorage_id = ?;",(ref,))  
                conn.commit()
            elif "EC" == x:
                conn.execute("DELETE FROM E_collector WHERE Ecollector_id = ?;",(ref,))  
                conn.commit()
            elif "DM" == x:
                conn.execute("DELETE FROM Decision_making_method WHERE DMaking_id = ?;",(ref,))  
                conn.commit()                

        print("DeRegistration Completed...")
        conn.close() 

    async def render_delete(self, request):
        print("\nRecv: DEREG_Request from {}".format(request.remote.hostinfo))
        print("{}".format(request))
        data = json.loads(request.payload)
        #print(json.dumps(data))

        conn = sqlite3.connect(DB_name)
        cursor_obj = conn.cursor()
        sql = "select COUNT(*) from Service_Registration where Reg_id  = ? "
        cursor_obj.execute(sql, (data['ref'],))
        count = cursor_obj.fetchone()[0]

        
        cursor_obj2 = conn.cursor()
        sql2 = "select COUNT(*) from roles where Role_id  = ? and role = ?"
        cursor_obj2.execute(sql2, (data['ref'], data['roles'][0],))
        count2 = cursor_obj2.fetchone()[0]
        if count > 0 and count2 > 0 :
            self.Del_DB(data['ref'], data['roles'])   
            print("\nResp: to {}".format(request.unresolved_remote))
            return aiocoap.Message(code=aiocoap.DELETED)
        else:
            payload = "Reference not found or Delegation roles not found".encode('ascii')
            print("DeRegistration Uncompleted...Reference not found or Delegation roles not found")
            print("\nResp: to {}".format(request.unresolved_remote))
            return aiocoap.Message(code=aiocoap.NOT_FOUND,payload=payload)
class lease_renew(resource.Resource):
    def __init__(self):
        super().__init__()

    def lease_update(self,ref,lease_time):
        
        conn = sqlite3.connect(DB_name)
        conn.execute("UPDATE Service_Registration set Lease_time = ? where Reg_id = ?;",(lease_time,ref,))  
        conn.commit()
        print("Lease time renewal completed...")
        conn.close() 

    async def render_put(self, request):
        print("\nRecv: Lease_Renewal_Request from {}".format(request.unresolved_remote))
        print("{}".format(request))
        data = json.loads(request.payload)
        #print(json.dumps(data, indent=4))
        #print(json.dumps(data))
        leasing_time = datetime.timestamp(datetime.now())+data['lease_time']
        print('Registration Ref: %s\nNew registration expiry: %s'%(data['ref'],datetime.fromtimestamp(int(leasing_time))))
        #print(int(leasing_time))
        #print(datetime.fromtimestamp(int(leasing_time)))

        conn = sqlite3.connect(DB_name)
        cursor_obj = conn.cursor()
        sql = "select COUNT(*) from Service_Registration where Reg_id  = ? "
        cursor_obj.execute(sql, (data['ref'],))
        count = cursor_obj.fetchone()[0]
        if count > 0:
            self.lease_update(data['ref'], leasing_time)  
            print("\nResp: to {}".format(request.unresolved_remote))        
            return aiocoap.Message(code=aiocoap.CHANGED)
        else:
            payload = "Reference not found ".encode('ascii')
            print("Lease time renewal Uncompleted...Reference not found")
            print("\nResp: to {}".format(request.unresolved_remote))
            return aiocoap.Message(code=aiocoap.NOT_FOUND,payload=payload)
class Delegate_Lookup(resource.Resource):
    def __init__(self):
        super().__init__()
        
    def lookup(self, roles, t_model, e_storage, e_collector, d_maker ):
        #print(roles)
        print('Looking up Roles: %s'%(roles))
        conn = sqlite3.connect(DB_name)
        sql = "select Role_id from roles where role in %s" % repr(roles).replace('[','(').replace(']',')') 
        
        # select IP_Address of delegate(s) providing specific trust models 
        TC_list=[]
        TC_IPlist=[]
        if "TC" in roles:
            sql2 = "select TModel_id from Trust_model where Trust_model in %s" % repr(t_model).replace('[','(').replace(']',')')
            for row in conn.execute(sql2):
                TC_list.append(row[0])
            #print(TC_list)  
            sqlip = "select Delegate_ip from Service_Registration where Reg_id in %s" % repr(TC_list).replace('[','(').replace(']',')')
            for row2 in conn.execute(sqlip):
                TC_IPlist.append(row2[0])
            #print(TC_IPlist) 
            print('TC IP: %s'%(TC_IPlist))
        
        # select IP_Address of delegate(s) providing the trust repositor role
        TR_list=[]
        TR_IPlist=[]
        if "TR" in roles:
            sql2 = "select Estorage_id from E_storage where evidence in %s" % repr(e_storage).replace('[','(').replace(']',')')
            for row in conn.execute(sql2):
                TR_list.append(row[0])
            #print(TR_list) 
            sqlip = "select Delegate_ip from Service_Registration where Reg_id in %s" % repr(TR_list).replace('[','(').replace(']',')')
            for row2 in conn.execute(sqlip):
                TR_IPlist.append(row2[0])
            print('TR IP: %s'%(TR_IPlist))
        
        # select IP_Address of delegate(s) providing the trust evidence collector role
        EC_list=[]
        EC_IPlist=[]
        if "EC" in roles:
            sql2 = "select Ecollector_id from E_collector where evidence in %s" % repr(e_collector).replace('[','(').replace(']',')')
            for row in conn.execute(sql2):
                EC_list.append(row[0])
            #print(EC_list) 
            sqlip = "select Delegate_ip from Service_Registration where Reg_id in %s" % repr(EC_list).replace('[','(').replace(']',')')
            for row2 in conn.execute(sqlip):
                EC_IPlist.append(row2[0])
            print('EC IP: %s'%(EC_IPlist))
        
        # select IP_Address of delegate(s) providing the decision maker role
        DM_list=[]
        DM_IPlist=[]
        if "DM" in roles:
            sql2 = "select 	DMaking_id from Decision_making_method where Decision_making in %s" % repr(d_maker).replace('[','(').replace(']',')')
            for row in conn.execute(sql2):
                DM_list.append(row[0])
            #print(DM_list) 
            sqlip = "select Delegate_ip from Service_Registration where Reg_id in %s" % repr(DM_list).replace('[','(').replace(']',')')
            for row2 in conn.execute(sqlip):
                DM_IPlist.append(row2[0])
            print('DM IP: %s'%(DM_IPlist))
        #combine all ip    
        delegate_ip = {
      "TC": TC_IPlist,
      "TR": TR_IPlist,
      "EC": EC_IPlist,
      "DM": DM_IPlist,
    }
        #print(delegate_ip)
       # print(list(data.fetchall()))
        conn.close()
        return delegate_ip
        
    async def render_get(self, request):
        data = json.loads(request.payload)
        #print(json.dumps(data))
        print("\nRecv: Delegate_Lookup from {}".format(request.remote.hostinfo))
        print("{}".format(request))
        payload=self.lookup(data['roles'], data['t_model'], data['e_storage'], data['e_collector'], data['d_maker'])

        if not any(payload.values()):
            payload = "No delegates found".encode('ascii')
            print("Lookup Completed...No delegates found")
            print("\nResp: to {}".format(request.unresolved_remote))
            return aiocoap.Message(code=aiocoap.NOT_FOUND,payload=payload)
        else:
            print("Lookup Completed...")
            payload = json.dumps(payload)
            payload = payload.encode('ascii')
            print("\nResp: to {}".format(request.unresolved_remote))
            return aiocoap.Message(payload=payload)
        

                



async def main():
    # Resource tree creation
    global root
    root = resource.Site()
 
    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(['REG_Request'], Register())
    root.add_resource(['DEREG_Request'], DeRegister())
    root.add_resource(['Delegate_Lookup'], Delegate_Lookup())
    root.add_resource(['Lease_Renewal_Request'], lease_renew())
    await aiocoap.Context.create_server_context(root)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
