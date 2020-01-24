import socket
import sys
from math import *

def calculate(exp):
	# e1, op, e2 = exp.split()
	try:
		return eval(exp)
	except Exception as e:
		return str(e)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connection created")

in_port = 11111

# host_ip = socket.gethostbyname('www.google.com')
# s.connect((host_ip, port))
# print('Socket successfully created')

s.bind(('', in_port))
print("Bind complete")

s.listen(5)
print("Listening ...")

while True:
	con, client_addr = s.accept()
	print("Connection established with ", str(client_addr))
	msg = str.encode("Thanks for connecting, " + str(client_addr))
	# con.send("Thanks for connecting, " + client_addr)
	con.send(msg)

	rec = con.recv(1024).decode()
	while rec.upper() != 'EXIT':
		# Take action
		ans = calculate(rec)
		msg = str(ans)
		send_msg = "SERVER : " + msg
		con.send(str.encode(send_msg))
		rec = con.recv(1024).decode()

	print("Connection closed with " + str(client_addr))
	msg = "CON_ABORT"
	con.send(msg.encode())
	con.close()
