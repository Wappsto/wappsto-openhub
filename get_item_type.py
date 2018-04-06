from connect import Connect as connect
import requests
import json
import ast
import uuid



class Itemsvalue:

  def set_values(self,vid,vname,vpermission,vtype,nid,deviceid,option): 
    
    if option=='String':
      self.String_values(vid,vname,vpermission,vtype,nid,deviceid)
    elif option=='PercentType':
      self.PercentType_values(vid,vname,vpermission,vtype,nid,deviceid)
    elif option=='Decimal':
      self.Decimal_values(vid,vname,vpermission,vtype,nid,deviceid)
    else:
      print('did not work')
      print(option)


  def String_values(self,vid,vname,vpermission,vtype,nid,deviceid):
    
   string = {}
   string['max'] = 100
 
   value={}
   value[':id']=vid
   value[':type']='urn:seluxit:xml:bastard:value-1.1'
   value['name']= vname
   value['permission']=vpermission
   value['type']=vtype
   value['string']=string

   results=connect.get_value(value,nid,deviceid)
   self.send_value(results) 
  
  def PercentType_values(self,vid,vname,vpermission,vtype,nid,deviceid):

   number={}
   number['min']=0
   number['max']=100
   number['step']=1
 
   value={}
   value[':id']=vid
   value[':type']='urn:seluxit:xml:bastard:value-1.1'
   value['name']= vname
   value['permission']=vpermission
   value['type']=vtype
   value['number']=number

   results=connect.get_value(value,nid,deviceid)
   self.send_value(results)

 
  def Decimal_values(self,vid,vname,vpermission,vtype,nid,deviceid):

   number={}
   number['min']=0
   number['max']=1000000000000 #in openhab its java big decimal
   number['step']=0.1
 
   value={}
   value[':id']=vid
   value[':type']='urn:seluxit:xml:bastard:value-1.1'
   value['name']= vname
   value['permission']=vpermission
   value['type']=vtype
   value['number']=number
  
   results=connect.get_value(value,nid,deviceid)
   self.send_value(results)


  def send_value(self,value_data):   

   socket = connect.connect_to_server()
   message = connect.get_message('POST',value_data)
   connect.send(message,socket)
