import socket 
import json
from server import global_port as port

def intialization(sck):
	'''
	For creating account or logging in
	'''

	print("\nYour option - \n(1) Create an account\n(2) Log in")
	choice = int(input("\nYour Choice (1 or 2) : "))

	if choice == 1 or choice == 2:
		pid = input("Enter Unique PID : ")
		password = input("Enter Password : ")

		message = {
			"type": "SIGN_UP" if choice == 1 else "LOG_IN",
			"pid": pid,
			"password": password
		}

		message = json.dumps(message)
		sck.sendall(message.encode())

	else:
		print("\n### Choose a correct option ###")
		intialization(sck)


def send_req(sck):
	'''
	Send request to server after successful login
	'''
	data = input()
	pass


if __name__ == '__main__':
	host = '127.0.0.1'

	# Establisihing connection to server
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	s.connect((host, port))
	print("\n### Connection Established ###\n")

	# Account creation or Log in
	intialization(s)

	while True: 
		# Receive data from server
		data = json.loads(s.recv(4096).decode())
		d_type = data["type"]

		if d_type == "SIGN_UP" or d_type == "LOG_IN":
			status, message = data["status"], data["message"]
			print("\n" + message)

			if status == 400:	
				break

			else:
				if d_type == "SIGN_UP":
					break

				else:
					# Send some req to server
					send_req(s)

		else:
			pass
	
	s.close() 