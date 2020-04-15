import socket 
from _thread import *
import threading 
import json
from os import listdir
from os.path import isfile, join
import account as acc
import log_handling as logh

global_port = 12356

def threaded_client(con, sckt, addr):
	'''
	Threaded function. Each thread is assigned to listen for one client and respond to them
	'''
	client_pid = None

	while True:
		try:
			# msg = {}
			# Received data from client
			msg = con.recv(4096).decode()
			data = json.loads(msg)

			if not data: 
				print("\n### [", addr, "] Disconnected ###\n")
				break

			else:
				type = data["type"]

				if type == "SIGN_UP" or type == "LOG_IN":
					pid, password = data["pid"], data["password"]
					client_pid = pid

					ret_data = acc.create_account(pid, password, addr) if type == "SIGN_UP" else acc.login(pid, password, addr)

					print(addr, ":", ret_data["message"])

					ret_data["type"] = type
					message = json.dumps(ret_data)
					con.sendall(message.encode())

					# If Log in or account creation fails, abort
					if ret_data["status"] == 400 or type == "SIGN_UP":
						break

					else:
						acknowledgement = json.loads(con.recv(4096).decode())
						
						if acknowledgement["type"] == "ACK":
							notifications = logh.retrieve_unread_notifications(pid)
							message = json.dumps({
								"type" : "UNREAD_NOTIFICATIONS",
								"message": { k:v for k,v in enumerate(notifications) }
							})
							con.sendall(message.encode())

						else:
							break

				elif type == "LOG_OUT":
    				# Logging out of the system
					acc.logout(pid)

					message = json.dumps({
						"type": "LOG_OUT_ACK",
						"message": "You are logged out"
					})
					con.sendall(message.encode())
					break

				elif type == "TRANSACTION":
					# Transaction
					credit, amount = data["credit"], data["amount"]

					debit_log = json.dumps({
						"TYPE": "DEBIT",
						"FROM": client_pid,
						"TO": credit,
						"AMOUNT": amount
					})

					credit_log = json.dumps({
						"TYPE": "CREDIT",
						"FROM": credit,
						"TO": client_pid,
						"AMOUNT": amount
					})

					debit_notification = "$" + str(amount) + " debited from your account and credited to " + credit + ""
					credit_notification = "$" + str(amount) + " credited to your account, received from " + client_pid + ""

					# Saving transaction history
					status = logh.create_new_log(credit, credit_log)

					if status:
						logh.create_new_log(client_pid, debit_log)

						# Notify sender and receiver about successfult transaction
						logh.create_notification(client_pid, debit_notification, 'N')
						logh.create_notification(credit, credit_notification, 'N')

						client_note = logh.send_notifications_to_clients(client_pid)
						
						if client_note is None or client_note[0] is None:
							pass
						else:
							message = json.dumps({
								"type": "TRANSACTION",
								"status": 200,
								"message": debit_notification
							})
							con.sendall(message.encode())
						
					else:
						message = json.dumps({
							"type": "TRANSACTION",
							"status": 400,
							"message": "Transaction Failed! Invalid credit account"
						})
						con.sendall(message.encode())

				else:
					pass
			
		except KeyboardInterrupt:
			message = json.dumps({
				"type" : "FORCED_LOG_OUT",
			})
			# Account becomes passive
			acc.logout(client_pid)

			con.sendall(message.encode())
			sckt.close()
			break

		except Exception as e:
			# print(e)
			message = json.dumps({
				"type" : "FORCED_LOG_OUT",
			})
			# Account becomes passive
			acc.logout(client_pid)

			con.sendall(message.encode())
			sckt.close()
			break


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