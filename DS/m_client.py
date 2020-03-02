import socket 
import json
from m_server import global_port as port
  
if __name__ == '__main__':
	host = '127.0.0.1'

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	s.connect((host, port)) 

	print("\nCLIENT : ")
	message = "REQ_RESOURCE_INFO"
	print(message)
	s.sendall(message.encode())

	while True: 
		# Receive data from server
		data = json.loads(s.recv(1024).decode())
		d_type = data['type']
		d_data = data['data']

		print("\nSERVER : \n")

		if d_type == "RESOURCE_INFO":
			print("All valid resources : ")

			for key, value in d_data.items():
				print("RC" + str(key), ')', value)

			print("\n! Type Resourcse code on the left to request a resource !\n" + 
				"And Type 'ACC<Resource number>' to access after request is granted\n" + 
				"Type 'REL<Resource number>' to release it")

		elif d_type == "INVALID_RESOURCE_REQ":
			print(d_data)

		elif d_type == "SESSION_EXPIRED":
			print(d_data)
			break

		elif d_type == "REQ_GRANTED" or d_type == "REQ_WAIT" or d_type == "REQ_FAIL":
			print(d_data)

		elif d_type == "REL_GRANTED" or d_type == "REL_FAIL":
			print(d_data)

		elif d_type == "ACC_GRANTED" or d_type == "ACC_FAIL":
			print(d_data)

		elif d_type == "ACC_INPUT":
			print(d_data)

		# Send a reply to server
		print("\nCLIENT : ")
		reply = input()

		if reply == "REQ":
			reply = "REQ_RESOURCE_INFO"
		
		s.sendall(reply.encode())
		# pass
	
	s.close() 