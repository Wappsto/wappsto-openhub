import socket
import time
import os
import ssl
import json
import datetime
import requests
import uuid

class Connect:


 def connect_to_server():# connects to server, sends data, receives data
  
  serverAddr = "q-wot.com"
  serverPort = 21005
  sslServerCert = "./certificates/ca.crt"
  sslClientCert =  "./certificates/client.crt"
  sslKey = "./certificates/client.key"
  
  myRawSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  mySocket = ssl.wrap_socket(myRawSocket, ca_certs=sslServerCert, certfile=sslClientCert, keyfile=sslKey, cert_reqs=ssl.CERT_REQUIRED)
  try:
   mySocket.settimeout(10)
   mySocket.connect((serverAddr, serverPort)) 
  except Exception as e:
    print("Failed to connect: %s" % str(e))
    return None
  else:
   connected = True
   return mySocket

 def get_network(network_id,network_name): #gets network information 
    
  network = {}
  network['name']=network_name # get from wappsto
  network[':id']= network_id 
  network[':type']='urn:seluxit:xml:bastard:network-1.1'
  
  url='/network/'
  
  params={}
  params['data']=network
  params['url']=url
  
  return params


 def get_device(device_id,device_name,network_id): #gets device information
 

  device={}
  device[':id']=device_id
  device[':type']='urn:seluxit:xml:bastard:device-1.1'
  device['name']=device_name
  device['included']='1'

  url='/network/'+network_id+'/device'
  
  params={}
  params['data']=device
  params['url']=url
  
  return params

 def get_value(passed_value,network_id,device_id): # add passed value which will choose number, string or blob
 
  url='/network/'+network_id+'/device/'+device_id+'/value'
 
  params={}
  params['data']=passed_value
  params['url']=url
  return params

 def get_state(state_id,state_data,network_id,device_id,value_id,state_type):
 
  time=datetime.datetime.now().isoformat()+'Z'
  state={}
  state[':id']= state_id
  state[':type']='urn:seluxit:xml:bastard:state-1.1'
  state['timestamp']=time
  state['data']= state_data
  state['type']= state_type
  url='/network/'+network_id+'/device/'+device_id+'/value/'+ value_id +'/state'
  params={}
  params['data']=state
  params['url']=url
  return params

 def send(message_to_send,socket):
  print(message_to_send)
  c=socket.send(message_to_send.encode('utf-8'))
  print('http code for intended change: {} '.format(c)),
  data = socket.recv(2000)
  decoded = json.loads(data.decode('utf-8'))
  print("Received data from server:")
  print(decoded)
  
 def get_message(method,choice):
 
  message={}
  message['jsonrpc']='2.0'
  message['id']='1'
  message['method']=method
  message['params']=choice 
  final_message=json.dumps(message)
  return final_message

 