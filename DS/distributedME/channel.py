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
	local_server["state"] = []

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
	t2 = threading.Thread(target=trigger)
	t1.start()
	t2.start()


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


def trigger():
	global req_arr
	global def_arr

	while True:
		try:
			f = open("resource.pkl", "rb")
			rec_dict = pickle.load(f)
			f.close()

			hold = list(filter(lambda x: x[1] == "BUSY", local_server["state"]))
			for pid, state in hold:
				if rec_dict[int(pid)]["available"] > 0:
					for addr, pr_id in def_arr:
						if int(pid) == int(pr_id):
							message = json.dumps({
								"type": "REP",
								"from": local_server,
								"resource": int(pid)
							})

							# print("hello")

							sender(addr, message)

							print("\nReply to", addr, "to grant access to #Resource", str(pid) + "#")

					def_arr = list(filter(lambda x: x[1] != int(pid), def_arr))

		except Exception as e:
			pass


def handler(data):
	global req_arr

	f = open("resource.pkl", "rb")
	rec_dict = pickle.load(f)
	f.close()
	# print()

	d_type = data["type"]
	cont = True

	if d_type == "EXIT":
		cont = False
	else:
		d_sen = data["from"]
		d_rec = int(data["resource"])

		if d_type == "REQ":

			print("\nRequest from [", d_sen["addr"], "-", d_sen["port"], "] for #Resource", str(d_rec) + "#")

			if ([int(d_rec), "BUSY"] in local_server["state"] and rec_dict[d_rec]["available"] == 0) or ([int(d_rec), "QUEUED"] in local_server["state"] and local_server["timestamp"] < d_sen["timestamp"] and rec_dict[d_rec]["available"] == 0):
				def_arr.append([[d_sen["addr"], d_sen["port"]], int(d_rec)])
				# print("hello")
			else:
				message = json.dumps({
					"type": "REP",
					"from": local_server,
					"resource": int(d_rec)
				})

				sender((d_sen["addr"], d_sen["port"]), message)
				print("\nReply to [", d_sen["addr"], "-", d_sen["port"], "] to grant access to #Resource", str(d_rec) + "#")

		elif d_type == "REP":

			print("\nReply from [", d_sen["addr"], "-", d_sen["port"], "] of #Resource", str(d_rec) + "#")
			# print("rem")
			try:
				req_arr.remove([[d_sen["addr"], d_sen["port"]], int(d_rec)])
			except Exception as e:
				pass

	# print(local_server)
	# print(req_arr)
	# print(def_arr)

	return cont


def req_cs(resource_id):
	f = open("active.pkl", "rb")
	data = pickle.load(f)
	os.environ["all_process"] = json.dumps(data)
	f.close()

	local_server["timestamp"] = time.time()
	local_server["state"].append([int(resource_id), "QUEUED"])

	message = json.dumps({
		"type": "REQ",
		"from": local_server,
		"resource": int(resource_id)
	})

	for pid, addr in json.loads(os.environ["all_process"]).items():
		if int(pid) != int(local_server["id"]):
			sender(addr, message)
			print("\nRequest for #Resource", str(resource_id) + "#", "sent to", addr)
			req_arr.append([list(addr), int(resource_id)])

	while len(list(filter(lambda x: x[1] == int(resource_id), req_arr))) > 0:
		pass

	local_server["state"].remove([int(resource_id), "QUEUED"])
	local_server["state"].append([int(resource_id), "BUSY"])

	print("\n### Resource", resource_id, ": ACQUIRED : Entering Critical Section ### ")

	f = open("resource.pkl", "rb")
	rec_dict = pickle.load(f)
	f.close()

	# print(rec_dict[resource_id]["available"])

	rec_dict[int(resource_id)]["holder"].append([local_server["addr"], local_server["port"]])
	rec_dict[int(resource_id)]["available"] = rec_dict[int(resource_id)]["available"] - 1

	f = open("resource.pkl", "wb")
	pickle.dump(rec_dict, f)
	f.close()


def rel_cs(resource_id):
	f = open("active.pkl", "rb")
	data = pickle.load(f)
	os.environ["all_process"] = json.dumps(data)
	f.close()

	f = open("resource.pkl", "rb")
	rec_dict = pickle.load(f)
	f.close()

	# print(rec_dict[int(resource_id)]["available"])
	rec_dict[int(resource_id)]["available"] = rec_dict[int(resource_id)]["available"] + 1
	rec_dict[int(resource_id)]["holder"].remove([local_server["addr"], local_server["port"]])

	print("\n### Resource", resource_id, ": RELEASED : Exiting Critical Section ### ")

	# print(rec_dict[int(resource_id)]["available"])

	# if int(rec_dict[int(resource_id)]["available"]) == 1:
	# 	print(rec_dict[int(resource_id)]["holder"])
	# 	for addr in rec_dict[int(resource_id)]["holder"]:
	# 		message = json.dumps({
	# 			"type": "REP",
	# 			"from": {
	# 				"addr": addr[0],
	# 				"port": addr[1],
	# 			},
	# 			"resource": int(resource_id)
	# 		})

	# 		sender(addr, message)

	f = open("resource.pkl", "wb")
	pickle.dump(rec_dict, f)
	f.close()

	local_server["state"].remove([int(resource_id), "BUSY"])
	message = json.dumps({
		"type": "REP",
		"from": local_server,
		"resource": int(resource_id)
	})

	global def_arr
	for addr, res_id in def_arr:
		if int(res_id) == int(resource_id):
			sender(addr, message)
			print("\nRelease message of #Resource", str(resource_id) + "#", "sent to", addr)
	
	def_arr = list(filter(lambda x: x[1] != int(resource_id), def_arr))


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