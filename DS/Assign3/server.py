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

global_port = 12354
halt_process = False
deamon_processes = []
warning_phase = False
running_process = {}
error_detection_time = None


def cur_time():
	'''
	Return current time in terms of yyyy-mm-dd hh:mm:ss
	'''

	time_now = time.localtime()
	y, mo, d, h, mi, s = time_now.tm_year, time_now.tm_mon, time_now.tm_mday, time_now.tm_hour, time_now.tm_min, time_now.tm_sec

	timestamp = "{year}-{month}-{day} {hour}:{minute}:{second}".format(year=y, month=mo, day=d, hour=h, minute=mi, second=s)

	return timestamp


def background_error_check(sckt):
	'''
	Runs every 10 secs to check log inconsistency
	'''

	while True:
		try:
			# Check for error
			global deamon_processes
			global halt_process
			halt_process = True

			idly = list(running_process.values())
			# print("Start idle check loop")
			while "BUSY" in idly:
				idly = list(running_process.values())

			# print("End idle check loop")

			status, deamon_processes = er.check_log_consistency()
			# print(status, deamon_processes)

			if not status:
				global warning_phase
				global error_detection_time

				warning_phase = True
				
				for pid in deamon_processes:
					acc.block(pid)
					# print(pid)

				all_process = acc.all_process()
				error_detection_time = cur_time()
				notification = "Deamon process detected at" + error_detection_time + " ! Processes - " + str(deamon_processes)

				for pid, status in all_process:
					if status != 'Y':
						logh.create_notification(pid, notification, 'N')

				# Recover from fault
				er.backward_error_recovery()

				halt_process = False

				# print("Start checking if all logged out")
				while len(running_process) != 0:
					pass

				# print("Stop in checking if all logged out")

				warning_phase = False

			else:
				er.create_checkpoint()
				deamon_processes = []
				halt_process = False
				warning_phase = False
				# print("\n---------------------------------\nBackground Error Detection Complete ... No error\n---------------------------------\n")

		except KeyboardInterrupt:
			pass
		except Exception as e:
			pass

		warning_phase = False
		halt_process = False
		time.sleep(10.0)


def threaded_client(con, sckt, addr):
	'''
	Threaded function. Each thread is assigned to listen for one client and respond to them
	'''
	
	client_pid, warning = None, False
	global running_process

	while True:

		try:
			# Received data from client
			print("\nWaiting for req. from", addr)
			msg = con.recv(4096).decode()
			data = json.loads(msg)
			print("Req. from", addr)

			if halt_process:
				print("Start in halt process loop")
				while halt_process:
					
					# print("\n### Server Busy fixing consistency! Waiting for response ... ###")
					pass

				print("End in halt process loop")

			if client_pid is None:
				client_pid = data["pid"]
				running_process[client_pid] = "NONE"

			if warning_phase:
				message = json.dumps({
					"type": "RESTART",
					"message": "Deamon process detected!",
					"process": { k:v for k,v in enumerate(deamon_processes) },
					"timestamp": error_detection_time
				})

				running_process.pop(client_pid)
				acc.logout(client_pid)
				con.sendall(message.encode())
				break
			
			running_process[client_pid] = "BUSY"

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

					message = json.dumps(ret_data)
					con.sendall(message.encode())

					# If Log in or account creation fails, abort
					if ret_data["status"] == 400 or type == "SIGN_UP":
						running_process.pop(client_pid)
						break

					else:
						client_log = json.dumps({
							"TYPE": "LOGIN",
							"TIMESTAMP": cur_time(),
							"STATUS": "SUCCESS"
						})

						logh.create_new_log(client_pid, client_log)

						print("\nWaitig from ACK from", addr)
						acknowledgement = json.loads(con.recv(4096).decode())
						print("\nACK from", addr)
						# print(acknowledgement)

						if acknowledgement["type"] == "ACK":
							notifications = logh.retrieve_unread_notifications(pid)
							message = json.dumps({
								"type" : "UNREAD_NOTIFICATIONS",
								"message": { k:v for k,v in enumerate(notifications) },
							})

							con.sendall(message.encode())

						else:
							running_process.pop(client_pid)
							break

				elif type == "LOG_OUT":
					# Logging out of the system
					acc.logout(pid)

					client_log = json.dumps({
						"TYPE": "LOGOUT",
						"TIMESTAMP": cur_time(),
						"STATUS": "SUCCESS"
					})

					logh.create_new_log(client_pid, client_log)

					message = json.dumps({
						"type": "LOG_OUT_ACK",
						"message": "You are logged out",
					})

					running_process.pop(client_pid)
					con.sendall(message.encode())
					break

				elif type == "TRANSACTION":
					# Transaction
					credit, amount = data["credit"], data["amount"]

					timestamp = cur_time()

					debit_log = {
						"TYPE": "DEBIT",
						"FROM": client_pid,
						"TO": credit,
						"AMOUNT": amount,
						"TIMESTAMP": timestamp
					}

					credit_log = json.dumps({
						"TYPE": "CREDIT",
						"FROM": credit,
						"TO": client_pid,
						"AMOUNT": amount,
						"TIMESTAMP": timestamp
					})

					debit_notification = "$" + str(amount) + " debited from your account and credited to " + credit + ""
					credit_notification = "$" + str(amount) + " credited to your account, received from " + client_pid + ""

					# Saving transaction history
					status = logh.create_new_log(credit, credit_log, False)

					if status:
						debit_log["STATUS"] = "SUCCESS"
						logh.create_new_log(client_pid, json.dumps(debit_log))

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
							})
							con.sendall(message.encode())
						
					else:
						debit_log["STATUS"] = "FAIL"
						logh.create_new_log(client_pid, json.dumps(debit_log))

						message = json.dumps({
							"type": "TRANSACTION",
							"status": 400,
							"message": "Transaction Failed! Invalid credit account (or) Credit Account is blocked for malicious activity",
						})
						con.sendall(message.encode())

				elif type == "REQ_LOG":
					client_log = logh.fetch_client_log(client_pid)

					for log in client_log:
						con.sendall(log)

					con.sendall("END_OF_FILE".encode())

				else:
					pass
			
			running_process[client_pid] = "IDLE"

		except KeyboardInterrupt:
			message = json.dumps({
				"type" : "FORCED_LOG_OUT",
			})
			# Account becomes passive
			acc.logout(client_pid)
			client_log = json.dumps({
				"TYPE": "LOGOUT",
				"TIMESTAMP": cur_time(),
				"STATUS": "SUCCESS"
			})
			logh.create_new_log(client_pid, client_log)

			running_process.pop(client_pid)

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
			client_log = json.dumps({
				"TYPE": "LOGOUT",
				"TIMESTAMP": cur_time(),
				"STATUS": "SUCCESS"
			})
			logh.create_new_log(client_pid, client_log)

			running_process.pop(client_pid)

			con.sendall(message.encode())
			sckt.close()
			break

		running_process[client_pid] = "IDLE"


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