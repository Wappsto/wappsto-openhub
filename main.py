from connect import Connect as connect
from openhab_data import Openhab
from threads import Threads
import json
import socket
import threading


#new_socket=connect.connect_to_server()
running=True

a=Openhab()
b=Threads()

#a.initialize()

while True:
	openhab_sending= threading.Thread(target=b.sending_thread) #thread for getting data from openhab sending to wappsto
	wappsto_sending= threading.Thread(target=b.receiving_thread) # thread for getting data from wappsto sending to openhab

	if running: 
		openhab_sending.start()
		wappsto_sending.start()
		openhab_sending.join()
		wappsto_sending.join()
	

	'''
#b=Threads()
b.sending_thread()
b.receiving_thread()'''