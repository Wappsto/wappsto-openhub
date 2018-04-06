from connect import Connect as connect
import requests
import os
import uuid_defines as my_ids
import json
import ast
import time



class Threads():

	def initialize(self):

		self.socket=connect.connect_to_server()
		self.network_id=my_ids.NETWORK_ID

	def sending_thread(self):

 		
 		self.initialize()
 		things=os.listdir('device')
 		for device in things:
 			content=os.listdir('device\\'+device)
 			if 'value' in content:
 				device_id=open('device\\'+device+'\\device_id.txt','r')
 				device_id=device_id.read()
 				value_names=os.listdir('device\\'+device+'\\value')
 				for value in value_names:
 					value_id=open('device\\'+device+'\\value\\'+value+'\\value_id.txt','r')
 					value_id=value_id.read()
 					state_id_r=open('device\\'+device+'\\value\\'+value+'\\state\\Report\\state_id.txt','r')
 					state_id_r=state_id_r.read()
 					state_id_c=open('device\\'+device+'\\value\\'+value+'\\state\\Control\\state_id.txt','r')
 					state_id_c=state_id_c.read()
 					
 					data=requests.get('http://localhost:8080/rest/items/'+value)
 					data=json.loads(data.content)
 					data=data.get('state')
 				
 					results=connect.get_state(state_id_r,data,self.network_id,device_id,value_id,'Report')
 					message = connect.get_message('POST',results)
 					connect.send(message,self.socket)

 					results=connect.get_state(state_id_c,data,self.network_id,device_id,value_id,'Control')
 					message = connect.get_message('POST',results)
 					connect.send(message,self.socket)
 				
 					time.sleep(5)
 					

	def receiving_thread(self):

 		#network_id=my_ids.NETWORK_ID
 		self.initialize()
 		things=os.listdir('device')
 		for device in things:
 			content=os.listdir('device\\'+device)
 			if 'value' in content:
 				device_id=open('device\\'+device+'\\device_id.txt','r')
 				device_id=device_id.read()
 				value_names=os.listdir('device\\'+device+'\\value')
 				for value in value_names:
 					value_id=open('device\\'+device+'\\value\\'+value+'\\value_id.txt','r')
 					value_id=value_id.read()
 					state_type='Control'
 					state_id=open('device\\'+device+'\\value\\'+value+'\\state\\Control\\state_id.txt','r')
 					state_id=state_id.read()
 					get_control_url='/network/'+self.network_id+'/device/'+device_id+'/value/'+ value_id +'/state/'+state_id
 					state_data=self.request_state('GET',get_control_url,self.socket)
 					time.sleep(10)
 					url_openhab='http://localhost:8080/rest/items/'+value
 					send=requests.post(url_openhab, data=state_data)


 					

	def request_state(self,method,url,socket): 

 		params={}
 		params['url']=url
 		message=connect.get_message(method,params)
 		socket.send(message.encode('utf-8'))
 		data = socket.recv(2000)
 		time.sleep(1)
 		data=json.loads(data)
 		time.sleep(1)
 		results=data.get('result')
 		results=ast.literal_eval(results)
 		time.sleep(1)
 		state=results.get('data')
 		return state
 		

 					
    


					
  
