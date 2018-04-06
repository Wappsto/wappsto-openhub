from get_item_type import Itemsvalue
from connect import Connect as connect
import requests
import os
import json
import uuid
import ast
import uuid_defines as my_ids
import shutil

class Openhab:

  def get_things(self): # gets names of all devices in openhab and returns them in list

   if not os.path.exists('device'):
   	os.makedirs('device')
   things=requests.get('http://localhost:8080/rest/things')
   allthings=json.loads(things.content) 
   length=(len(allthings))-1
   x=0
   y=0
   while x<=length:
     allthings=json.loads(things.content)[x]
     thing_name=allthings.get('label')
     results=allthings.get('channels')
     if not os.path.exists('device\\'+thing_name):
      os.makedirs('device\\'+thing_name)
      uid=str(uuid.uuid4())
      filename='device\\'+thing_name+'\\device_id.txt'
      f=open(filename,'w')
      f.write(uid)
      f.close()
      self.create_device(thing_name)
      lench=(len(results))-1
      if results:
     		while y<=lench:
     			linked=results[y]
     			channel=str(linked.get('linkedItems'))
     			new=channel[2:-2]
     			if new:
     				self.create_value_folder(new,thing_name)
     				self.set_value_name(new,thing_name)
     			y=y+1
     y=0 
     x=x+1

  def create_device(self,thing_name):

    network_id=my_ids.NETWORK_ID
    network_name= my_ids.NETWORK_NAME
    device_id=open('device\\'+thing_name+'\\device_id.txt','r')
    device_id=device_id.read()
    device_name=thing_name

    network_data=connect.get_network(network_id,network_name)
    self.send_data(network_data)
    device_data=connect.get_device(device_id,device_name,network_id)
    self.send_data(device_data)
    
  def set_value_name(self,ch_name,device_name):

  	address='http://localhost:8080/rest/items/'+ch_name
  	all_values = requests.get(address)
  	all_values = json.loads(all_values.content)
  	type_item=all_values.get('type')

  	if type_item=='Color':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Contact':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Dimmer':
  		v_name=ch_name
  		value_property='Decimal'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Location':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Number':
  		v_name=ch_name
  		value_property='Decimal'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Number:':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Player':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Rollershutter':
  		v_name=ch_name
  		value_property='PercentType'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='String':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  	elif type_item=='Switch':
  		v_name=ch_name
  		value_property='String'
  		self.channel_values(v_name,value_property,device_name)

  def channel_values(self,value_name,value_property,device_name): 

    network_id=my_ids.NETWORK_ID
    network_name=my_ids.NETWORK_NAME

    address='http://localhost:8080/rest/items/'+value_name
    all_values = requests.get(address)
    all_values = json.loads(all_values.content)
    v_permission= all_values.get('stateDescription')
    v_type = all_values.get('type')
    if v_permission:
      if "readOnly" in v_permission:
        v_permission='r'
    else:
      v_permission='rw'

    state=all_values.get('state')
    value_id=open('device\\'+ device_name +'\\value\\'+value_name+'\\value_id.txt','r')
    value_id=value_id.read()
    device_id=open('device\\'+device_name +'\\device_id.txt','r')
    device_id=device_id.read()


    q=Itemsvalue()
    q.set_values(value_id,value_name,v_permission,v_type,network_id,device_id,value_property)
    self.get_state(device_name,all_values,value_id,network_id,device_id,value_name)
 
  def create_value_folder(self,value_name,device_name):

  	uid=str(uuid.uuid4())
  	dir_name='device\\'+device_name+'\\value\\'+value_name
  	os.makedirs(dir_name)
  	f=open(dir_name+'\\value_id.txt','w')
  	f.write(uid)
  	f.close()
  	self.create_state_folder(dir_name,value_name,device_name)

  def create_state_folder(self,dir_name,value_name,device_name):

  	state_dir=dir_name+'\\state'
  	report=state_dir+'\\Report'
  	control=state_dir+'\\Control'
  	os.makedirs(report)
  	uid=str(uuid.uuid4())
  	f=open(report+'\\state_id.txt','w')
  	f.write(uid)
  	f.close()
  	os.makedirs(control)
  	uid=str(uuid.uuid4())
  	f=open(control+'\\state_id.txt','w')
  	f.write(uid)
  	f.close() 

  def get_state(self,device_name,datas,value_id,network_id,device_id,val_name):


   url_state='/network/'+network_id+'/device/'+device_id+'/value/'+value_id+'/state'
   state=datas.get('state')
   types=datas.get('type')
   
   report_id=open('device\\'+device_name+'\\value\\'+val_name+'\\state\\Report\\state_id.txt','r')
   report_id=report_id.read()
   
   control_id=open('device\\'+device_name+'\\value\\'+val_name+'\\state\\Control\\state_id.txt','r')
   control_id=control_id.read()

   data=state
   results=connect.get_state(report_id,data,network_id,device_id,value_id,'Report')
   self.send_data(results) 
   results=connect.get_state(control_id,data,network_id,device_id,value_id,'Control')
   self.send_data(results) 

  def send_data(self,state_data):   

    socket = connect.connect_to_server()
    message = connect.get_message('POST',state_data)
    connect.send(message,socket)
    print('data send')
  

  def requesting(self): # gets data from network based on url

    devices=os.listdir('device')
    for item in devices:
      item_id=open('device\\'+item+'\\device_id.txt','r')
      item_id=item_id.read()
      self.delete_device(item_id)

  def delete_device(self,item_id):

    nid=my_ids.NETWORK_ID
    delete_url='/network/'+nid+'/device/'+item_id
    func_method=str('DELETE')
    params={}
    params['url']=delete_url
    socket=connect.connect_to_server()
    message=connect.get_message(func_method,params)
    c=socket.send(message.encode('utf-8'))
    data = socket.recv(2000)
    decoded = json.loads(data.decode('utf-8'))
    return decoded

  def initialize(self):
    
    if os.path.exists('device'):
      self.requesting()
      shutil.rmtree('device', ignore_errors=True)
    self.get_things()
      


