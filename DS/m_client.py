import socket 
import json
  
  
if __name__ == '__main__':
	host = '127.0.0.1'
	port = 12345

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	s.connect((host,port)) 
  
	message = "REQ_CON"
	s.sendall(message.encode())

	while True: 
		data = s.recv(1024).decode()

		if data == "REQ_GRANTED":
			print("\nChoose your option : ")
			print("Option1 : Name of files in server-side")
			print("Option2 : Data Content of a file")
			print("Option3 : Log Out\n")

			option = int(input("Your Choice : "))
			print()

			if option == 1:
				msg = "OP#1"
			elif option == 2:
				msg = "OP#2"
			elif option == 3:
				msg = "OP#3"
			else:
				msg = "OP#INVALID"
			
		elif data == "REQ_FILENAME":
			msg = input("Enter Filename : ")

		elif data == "SESSION_EXPIRED":
			print("\n### Session Expired ###\n")
			break

		else:
			data = json.loads(data)
			typ = data["typ"]

			if typ == "FILELIST":
				print("\nAll the files in server directory : \n")
				content = data["content"]

				for file in content:
					print(file)
			else:
				print("\nData : \n")
				shift, d = data["shift"], data["content"]

				'''
				Decryption
				'''
				new_d = ""
				for ch in d:
					if 65+shift <= ord(ch) <= 90+shift or 97+shift <= ord(ch) <= 122+shift:
						new_d = new_d + chr(ord(ch) - shift)

					else:
						new_d = new_d + ch

				print(new_d)

			msg = "CONTINUE"
		
		s.sendall(msg.encode())
	
	s.close() 