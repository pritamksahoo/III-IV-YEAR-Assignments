import socket 
from _thread import *
import threading 
import json
import time
from os import listdir
from os.path import isfile, join
import account as acc
import log_handling as logh
import error_detection_recovery as er

global_port = 12352
halt_process = False
deamon_processes = []
warning_phase = 0


def check_warning_phase(wrn):
	'''
	Check whether client has been warned about deamon process
	'''
	if wrn != warning_phase:
		return warning_phase


def background_error_check(sckt):
	'''
	Runs every 30 secs to check log inconsistency
	'''

	while True:
		try:
			# Check for error
			global deamon_processes
			status, deamon = er.check_log_consistency()
			# print(status, deamon_processes)

			if not status:
				global halt_process
				global warning_phase

				halt_process = True
				warning_phase = 1 - warning_phase

				for pid in deamon_processes:
					acc.block(pid)
					# print(pid)

				all_process = acc.all_process()
				notification = "Deamon process detected! Process - " + str(deamon)

				if deamon_processes != deamon:
					deamon_processes = deamon.copy()
					for pid in all_process:
						logh.create_notification(pid, notification, 'N')

				# Recover from fault
				er.backward_error_recovery()

				halt_process = False

			else:
				print("\n---------------------------------\nBackground Error Detection Complete ... No error\n---------------------------------\n")

		except KeyboardInterrupt:
			pass
		except Exception as e:
			pass

		time.sleep(5.0)


def threaded_client(con, sckt, addr):
	'''
	Threaded function. Each thread is assigned to listen for one client and respond to them
	'''
	client_pid, warning = None, 0

	while True:

		try:
			# msg = {}
			# Received data from client
			msg = con.recv(4096).decode()
			data = json.loads(msg)

			while halt_process:
				print("\n### Server Busy fixing consistency! Waiting for response ... ###")
				pass

			# If current process is detected as deamon process, then blocked
			if client_pid in deamon_processes:
				message = json.dumps({
					"type" : "FORCED_BLOCK",
					"warning": True,
					"deamon_process": deamon_processes
				})
				# Account becomes passive
				acc.block(client_pid)

				con.sendall(message.encode())
				sckt.close()
				break

			# Handling request from client
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
					ret_data["warning"] = True if warning != warning_phase else False
					ret_data["deamon_process"] = deamon_processes

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
								"message": { k:v for k,v in enumerate(notifications) },
								"warning": True if warning != warning_phase else False,
								"deamon_process": deamon_processes
							})

							warning = check_warning_phase(warning)
							con.sendall(message.encode())

						else:
							break

				elif type == "LOG_OUT":
					# Logging out of the system
					acc.logout(pid)

					message = json.dumps({
						"type": "LOG_OUT_ACK",
						"message": "You are logged out",
						"warning": False
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
								"message": debit_notification,
								"warning": True if warning != warning_phase else False,
								"deamon_process": deamon_processes
							})
							warning = check_warning_phase(warning)
							con.sendall(message.encode())
						
					else:
						message = json.dumps({
							"type": "TRANSACTION",
							"status": 400,
							"message": "Transaction Failed! Invalid credit account (or) Credit Account is blocked for malicious activity",
							"warning": True if warning != warning_phase else False,
							"deamon_process": deamon_processes
						})
						warning = check_warning_phase(warning)
						con.sendall(message.encode())

				else:
					pass
			
		except KeyboardInterrupt:
			message = json.dumps({
				"type" : "FORCED_LOG_OUT",
				"warning": False
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
				"warning": False
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

	# Threaded function to check error in background
	t = threading.Thread(target=background_error_check, args=(sckt, ))
	t.start()

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
			break

		except Exception as e:
			sckt.close()
			break

	try:
		sckt.close() 
	except Exception as exp:
		pass