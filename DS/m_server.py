import socket 
from _thread import *
import threading 
import json
from os import listdir
from os.path import isfile, join

filepath = "/home/pks/Desktop/CODE/DS/"

pos_shift = 3

def threaded_client(c, s, addr): 
	while True:
		try:
			data = c.recv(1024).decode()

			if not data: 
				print("CON_ABORT")
				msg = "SESSION_EXPIRED"
				c.send(msg.encode())
				break

			else:
				if data == "REQ_CON":
					print("\nRequest to start communication [FROM] ", addr)
					msg = "REQ_GRANTED"
					c.sendall(msg.encode())
					print("Request Granted [", addr, "]")
				
				elif data == "OP#1":
					print("\nRequest to list all server files [FROM] ", addr)
					allfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
					msg = json.dumps({"typ" : "FILELIST", "content" : allfiles})
					c.sendall(msg.encode())
					print("Request Granted [", addr, "]")

				elif data == "OP#2":
					print("\nRequest content of a file [FROM] ", addr)
					msg = "REQ_FILENAME"
					c.sendall(msg.encode())
					
					data = c.recv(1024).decode()
					print("Filename [", addr, "] : ", data)

					with open(filepath + data, "r") as f:
						d = f.read()

					'''
					Encryption
					'''
					new_d = ""
					for ch in d:
						if 65 <= ord(ch.upper()) <= 90:
							new_d = new_d + chr(pos_shift + ord(ch))

						else:
							new_d = new_d + ch 

					msg = json.dumps({"typ": "FILECONTENT", "shift" : pos_shift, "content" : new_d})
					c.sendall(msg.encode())
					print("Request Granted [", addr, "]")

				elif data == "OP#3":
					msg = "SESSION_EXPIRED"
					c.sendall(msg.encode())

					break

				elif data == "OP#INVALID":
					print("\n### INVALID REQUEST ###\n")
					msg = "SESSION_EXPIRED"
					c.sendall(msg.encode())

					break

				elif data == "CONTINUE":
					msg = "REQ_GRANTED"
					c.sendall(msg.encode())
		
		except Exception as e:
			s.close()

	print("\n### Connection [", addr, "] Closed ###\n")
	c.close() 
  
  
if __name__ == '__main__': 
	host = "" 
	port = 12345

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host, port)) 

	print("### Socket binded to port ###", port) 

	s.listen(5) 
	print("socket is listening ...\n") 

	while True:
		c, addr = s.accept()
		print('Connected to :', addr[0], ':', addr[1]) 

		t1 = threading.Thread(target=threaded_client, args=(c,s,addr ))
		t1.start()

	s.close() 