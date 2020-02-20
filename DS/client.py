import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_port = 11111

# host_ip = socket.gethostbyname('www.google.com')
# s.connect((host_ip, port))
# print('Socket successfully created')

s.connect(('127.0.0.1', server_port))

# data = s.recv(1024).decode()
# print(data)
msg = "REQ"
s.send(msg.encode())

while data != "CON_ABORT":
	print(data)
	msg = input("YOU : ")
	s.send(msg.encode())
	data = s.recv(1024).decode()

print("!!!CONNECTION CLOSED!!!")
s.close()
