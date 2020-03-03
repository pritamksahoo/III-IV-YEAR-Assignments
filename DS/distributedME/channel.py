import socket 
from _thread import *
import threading 
import json
import os
# from os import listdir
# from os.path import isfile, join
# from resources import allocator as ra


local_server = {}
req_arr = []
def_arr = []


def add_new_con(host, port, pid):
	local_server["addr"] = host
	local_server["port"] = port
	local_server["id"] = pid

	if os.environ.get("all_process", None) is not None:
		os.environ.all_process[pid] = [host, port]
	else:
		os.environ["all_process"] = {}
		os.environ.all_process[pid] = [host, port]

	t1 = threading.Thread(target=listener)
	t1.start()


def sender(addr, port, msg):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(msg.encode(), (addr, port))
	s.close()


def listener():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((local_server["addr"], local_server["port"]))

	while True:
		try:
			message = json.loads(s.recv(4096).decode())
			ret = handler(message)

			if ret == False:
				print("### Connection with [", local_server['addr'], "] Closed ###\n")
				break

		except KeyboardInterrupt:
			s.close()

	s.close()


def handler(data):
	d_type = data['type']
	cont = True

	if d_type == "EXIT":
		cont = False
	else:
		d_rec = data['to']
		d_msg = data['msg']

		if d_type == "REQ":
			pass
		elif d_type == "REP":
			pass

	return cont


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