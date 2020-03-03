import socket 
from _thread import *
import threading 
import json
from os import listdir
from os.path import isfile, join
from resources import allocator as ra

# filepath = "/home/pks/Desktop/CODE/DS/"

global_port = 12345

resources = [(1, "Add two numbers"), (2, "Value of the global variable"), (3, "Increment the global variable")] 

def threaded_client(c, s, addr): 
	while True:
		try:
			# To store return message
			msg = {}
			# Received data from client
			data = c.recv(1024).decode()

			if not data: 
				print("\n### [", addr, "] Disconnected ###\n") 
				msg['type'] = "SESSION_EXPIRED"
				msg['data'] = "\n### Connection Terminated with server! ###\n"
				message = json.dumps(msg)
				c.sendall(message.encode())
				break

			else:
				if data == "REQ_RESOURCE_INFO":
					rec = dict(resources)
					msg['type'] = "RESOURCE_INFO"
					msg['data'] = rec
					message = json.dumps(msg)
					c.sendall(message.encode())

				elif data == "LOG_OUT":
					print("\n### [", addr, "] Connection Terminated ###\n")
					msg['type'] = "SESSION_EXPIRED"
					msg['data'] = "\n### Connection Terminated with server! ###\n"
					message = json.dumps(msg)
					c.sendall(message.encode())
					break

				elif data[:-1] == "RC":
					ret = ra.allocate(data, addr)
					if ret == "SUCCESS":
						msg['type'] = "REQ_GRANTED"
						msg['data'] = "Resource successfully allocated ! \nType 'ACC<Resource number>' to access !"
					elif ret == "WAIT":
						msg['type'] = "REQ_WAIT"
						msg['data'] = "Resource can't be allocated ! \nWAITING For Another process to release !"
					else:
						msg['type'] = "REQ_FAIL"
						msg['data'] = "Resource allocation failed ! \nTry again !"

					message = json.dumps(msg)
					c.sendall(message.encode())

				elif data[:-1] == "ACC":
					ret, val = ra.access(data, addr)
					if ret == "SUCCESS":
						msg['type'] = "ACC_GRANTED"
						msg['data'] = val
					elif ret == "ACC_WAIT_FOR_INPUT":
						msg['type'] = "ACC_INPUT"
						msg['data'] = val

						message = json.dumps(msg)
						c.sendall(message.encode())

						io = c.recv(1024).decode()
						ret, val = ra.access(data, addr, io)

						if ret == "SUCCESS":
							msg['type'] = "ACC_GRANTED"
							msg['data'] = val
						else:
							msg['type'] = "ACC_FAIL"
							msg['data'] = val
					else:
						msg['type'] = "ACC_FAIL"
						msg['data'] = "Permission to resource denied ! \nMake a request first !"

					message = json.dumps(msg)
					c.sendall(message.encode())

				elif data[:-1] == "REL":
					ret = ra.release(data, addr)
					if ret == "SUCCESS":
						msg['type'] = "REL_GRANTED"
						msg['data'] = "Resource successfully released !"
					else:
						msg['type'] = "REL_FAIL"
						msg['data'] = "No such allocation exists ! \nTry again !"

					message = json.dumps(msg)
					c.sendall(message.encode())

				else:
					msg['type'] = "INVALID_RESOURCE_REQ"
					msg['data'] = "!!! Choose a valid resource !!!"
					message = json.dumps(msg)
					c.sendall(message.encode())

		except KeyboardInterrupt:
			s.close()

	print("### Connection with [", addr, "] Closed ###\n")
	c.close() 
  
  
if __name__ == '__main__': 
	host = "127.0.0.1" 

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host, global_port)) 

	print("### Socket binded to port ###", global_port) 

	s.listen(5) 
	print("Socket is listening ...\n") 

	while True:
		try:
			c, addr = s.accept()
			print('Connected to :', addr[0], ':', addr[1]) 

			t1 = threading.Thread(target=threaded_client, args=(c, s, addr, ))
			t1.start()

		except KeyboardInterrupt:
			s.close()

	s.close() 