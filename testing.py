import requests
import os


things=os.listdir('device')
for device in things:
	content=os.listdir('device\\'+device)
	if 'value' in content:
 		device_id=open('device\\'+device+'\\device_id.txt','r')
 		device_id=device_id.read()
 		value_names=os.listdir('device\\'+device+'\\value')
 		for value in value_names:
 			state_data='0'
 			send=requests.post('http://localhost:8080/rest/items/hue_0210_0017887911f3_2_color_temperature', data= state_data)
 			print(send.status_code)