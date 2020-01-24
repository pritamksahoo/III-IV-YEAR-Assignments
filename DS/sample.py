import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_port = 8019

# host_ip = socket.gethostbyname('www.google.com')
# s.connect((host_ip, port))
# print('Socket successfully created')

s.bind(('127.0.0.1', server_port))

data = s.recv(1024)
s.close()
