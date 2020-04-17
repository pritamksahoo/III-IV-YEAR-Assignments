import socket 
import json
import os
from server import global_port as port

log_path = None

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


def send_req(sck, data):
	'''
	Send requests and handle response to and from server after successful login
	'''

	print("\nYour option - \n(1) Send Money\n(2) Request for client log\n(3) Log Out")
	choice = int(input("\nYour choice (1,2,3) : "))

	if choice == 1:
		credit_acc = input("\nCredit account PID : ")
		amount = float(input("Enter amount : "))

		message = json.dumps({
			"type": "TRANSACTION",
			"credit": credit_acc,
			"amount": amount
		})
		print("\nTransaction processing ...", end=' ')
		sck.sendall(message.encode())

	elif choice == 2:
		global log_path
		log_path = input("Enter your directory name (with full path) where log will be fetched : ")

		if os.path.isdir(log_path):
			with open(log_path + "log.txt", "w") as f:
				f.write("")

			print("\nFetching log ... processing ... ", end='')

			message = json.dumps({
				"type": "REQ_LOG",
			})

			with open(log_path + "log.txt", "w") as f:
				sck.sendall(message.encode())

				while True:
					# Receving data in chunk of 1024 B
					data = sck.recv(1024).decode()
					if data == "END_OF_FILE":
						break

					else:
						f.write(data)

					sck.sendall("NEXT".encode())

			print("Done\n### Log saved in " + log_path + "log.txt ###")

			inp = input("\nEnter anything to send back the file : ")

			if inp:
				sck.sendall("READY".encode())

				d = sck.recv(1024).decode()
				if d == "READY":
					print("\nSending back log file ... processing ... ", end="")

					fr = open(log_path + "log.txt", "rb")
					content = []
					log = fr.read(1024)
					while log:
						content.append(log)
						log = fr.read(1024)

					fr.close()

					for l in content:
						sck.sendall(l)
						d = sck.recv(1024).decode()
						if d == "NEXT":
							pass
						else:
							break

					sck.sendall("END_OF_FILE".encode())

					print("Done")

		else:
			print("\n!!! Directory path is invalid !!!")
			log_path = None

	elif choice == 3:
		# Log out
		log_out(sck)
		return False	

	else:
		print("\n### Choose a correct option ###")
		send_req(sck, data)

	return True


def log_out(sck):
	'''
	Logging out of client account. Due to any exception, server not responding, or keyboard interrupt like Ctrl-C or normal log out by client manually
	'''

	message = json.dumps({
		"type": "LOG_OUT"
	})
	sck.sendall(message.encode())

	data = json.loads(sck.recv(4096).decode())
	if data["type"] == "LOG_OUT_ACK":
		print("\n### " + data["message"] + " ###\n")

	else:
		print("\n### Server is not responding! Logged of the system ###\n")


if __name__ == '__main__':
	host = '127.0.0.1'

	# Establisihing connection to server
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	s.connect((host, port))
	print("\n### Connection Established ###\n")

	# Account creation or Log in
	intialization(s)
	state = True

	while True: 
		# Receive data from server
		try:
			if not state:
				break

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
						message = json.dumps({
							"type": "ACK"						
						})
						s.sendall(message.encode())

						# Fetching any outstanding notifications
						notifications = json.loads(s.recv(4096).decode())
						
						if notifications["type"] == "UNREAD_NOTIFICATIONS":
							unread_notifications = notifications["message"]
							# print(unread_notifications)
							print('\n------------------------------')
							if len(unread_notifications) == 0:
								print("### You have no unread notifications ###")

							else:
								print("### Notifications ###\n")
								for note in unread_notifications:
									print(unread_notifications[note])

							print('------------------------------')

						elif notifications["type"] == "RESTART":
							data = notifications
							print(data["timestamp"], "-::-",  data["message"])
							print(list(data["process"].values()))
							print("\n### You have been logged out! Login again")

							intialization(s)

						else:
							break

						# Start transactions
						state = send_req(s, data)

			elif d_type == "FORCED_LOG_OUT":
				print("\n### Server is not responding! Logging out of the system ###\n")
				break

			elif d_type == "FORCED_BLOCK":
				print("\n### Your account has been blocked due to log hijacking ###\n")
				break

			elif d_type == "TRANSACTION":
				status, message = data["status"], data["message"]
				print("Done")

				print("\n------------------------------\nTransaction stautus :", status)
				print(message)
				print('------------------------------')

				state = send_req(s, data)

			elif d_type == "RESTART":
				print("[ " + data["timestamp"] + " ] :",  data["message"])
				print("Processes ::", list(data["process"].values()))
				print("\n### System has been reverted back to stable state ###")
				print("\n### You have been logged out! Login again ###")

				# intialization(s)
				break

			elif d_type == "REQ_LOG":
				if data["status"] == 200:
					print("\n" + data["message"])

				send_req(s, data)

			else:
				# Start transactions
				state = send_req(s, data)

		except KeyboardInterrupt:
			# Log Out before client disconnects
			log_out(s)
			break

		except Exception as e:
			print(e)
			# Log Out before client disconnects
			log_out(s)
			break
	
	# END of Session
	s.close()