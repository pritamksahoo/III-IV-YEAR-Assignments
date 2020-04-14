import sys
import channel as ch
import numpy as np
import os
import json
import pickle


if __name__ == '__main__':

	f = open("active.pkl", "rb")
	data = pickle.load(f)
	# data = {}
	os.environ["all_process"] = json.dumps(data)

	if os.environ.get("all_process", None) is None:
		os.environ["all_process"] = json.dumps({})

	pid = np.random.randint(1, 100)
	while json.loads(os.environ["all_process"]).get(pid, None) is not None:
		pid = np.random.randint(1, 100)

	port = np.random.randint(1000, 9999)

	ch.add_new_con("127.0.0.1", port, pid)

	print("\nProcess :", pid, "| [ '127.0.0.1',", port, "]")

	while True:
		message = input()

		if message.lower()[:3] == "req":
			ch.req_cs(int(message[4:]))
			# print("Lock acquired")
		elif message.lower()[:3] == "rel":
			ch.rel_cs(int(message[4:]))
			# print("Lock released")