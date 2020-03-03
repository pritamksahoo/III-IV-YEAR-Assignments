import socket 
from _thread import *
import threading 
import json
import os
import pickle
import time
# from os import listdir
# from os.path import isfile, join
# from resources import allocator as ra


local_server = {}
req_arr = []
def_arr = []


def add_new_con(host, port, pid):
	f = open("active.pkl", "rb")
	data = pickle.load(f)
	os.environ["all_process"] = json.dumps(data)
	f.close()

	local_server["addr"] = host
	local_server["port"] = port
	local_server["id"] = pid
	local_server["state"] = "FREE"

	if os.environ.get("all_process", None) is not None:
		env = json.loads(os.environ["all_process"])
		env[pid] = (host, port)
		os.environ["all_process"] = json.dumps(env)
	else:
		env = {}
		env[pid] = (host, port)
		os.environ["all_process"] = json.dumps(env)

	f = open("active.pkl", "wb")
	pickle.dump(json.loads(os.environ["all_process"]), f)
	f.close()

	t1 = threading.Thread(target=listener)
	t1.start()


def sender(addr, msg):
	addr = tuple(addr)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(msg.encode(), addr)
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
	print(local_server)
	print(req_arr)
	print(def_arr)
	# print()

	d_type = data["type"]
	cont = True

	if d_type == "EXIT":
		cont = False
	else:
		d_sen = data["from"]

		if d_type == "REQ":
			if local_server["state"] == "BUSY" or (local_server["state"] == "QUEUED" and local_server["timestamp"] < d_sen["timestamp"]):
				def_arr.append([d_sen["addr"], d_sen["port"]])
			else:
				message = json.dumps({
					"type": "REP",
					"from": local_server,
				})

				sender((d_sen["addr"], d_sen["port"]), message)

		elif d_type == "REP":
			req_arr.remove([d_sen["addr"], d_sen["port"]])

	return cont


def req_cs():
	f = open("active.pkl", "rb")
	data = pickle.load(f)
	os.environ["all_process"] = json.dumps(data)
	f.close()

	local_server["timestamp"] = time.time()
	local_server["state"] = "QUEUED"

	message = json.dumps({
		"type": "REQ",
		"from": local_server, 
	})

	for pid, addr in json.loads(os.environ["all_process"]).items():
		if int(pid) != int(local_server["id"]):
			sender(addr, message)
			req_arr.append(list(addr))

	while len(req_arr) > 0:
		pass


def rel_cs():
	f = open("active.pkl", "rb")
	data = pickle.load(f)
	os.environ["all_process"] = json.dumps(data)
	f.close()

	local_server["state"] = "FREE"
	message = json.dumps({
		"type": "REP",
		"from": local_server,
	})

	for pid, addr in json.loads(os.environ["all_process"]).items():
		if int(pid) != int(local_server["id"]):
			sender(addr, message)
			def_arr.remove(addr)


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