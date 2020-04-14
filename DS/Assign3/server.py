import socket 
from _thread import *
import threading 
import json
from os import listdir
from os.path import isfile, join
import account as acc

global_port = 1231

def threaded_client(con, sckt, addr):
	'''
	Threaded function. Each thread is assigned to listen for one client and respond to them
	'''

	while True:
		try:
			msg = {}
			# Received data from client
			data = json.loads(con.recv(4096).decode())

			if not data: 
				print("\n### [", addr, "] Disconnected ###\n")
				break

			else:
				type = data["type"]

				if type == "SIGN_UP" or type == "LOG_IN":
					pid, password = data["pid"], data["password"]

					ret_data = acc.create_account(pid, password, addr) if type == "SIGN_UP" else acc.login(pid, password, addr)

					print(addr, ":", ret_data["message"])

					ret_data["type"] = type
					message = json.dumps(ret_data)
					con.sendall(message.encode())

					# If Log in or account creation fails, abort
					if ret_data["status"] == 400 or type == "SIGN_UP":
						break

				else:
					pass
			
		except KeyboardInterrupt:
			sckt.close()

	print("### Connection with [", addr, "] Closed ###\n")
	con.close() 
  
  
if __name__ == '__main__': 
	host = "127.0.0.1" 

	# Creating socket for listening to clients
	sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sckt.bind((host, global_port))
	print("\n### Socket binded to port -", global_port, "###") 

	# Listen upto maximum 5 clients
	sckt.listen(5) 
	print("Socket is listening ...\n") 

	while True:
		try:
			# Accepting clients' connection
			con, addr = sckt.accept()
			print('\nConnected to :', addr[0], ':', addr[1]) 

			# Assigning a thread to an individual client
			t1 = threading.Thread(target=threaded_client, args=(con, sckt, addr, ))
			t1.start()

		except KeyboardInterrupt:
			sckt.close()

	sckt.close() 