def update():
	'''
	To increment a global variable
	'''
	with open("var.txt", "r+") as f:
		line = f.read()

	var = int(line)
	var = var + 5

	with open("var.txt", "w+") as f:
		f.write(str(var))

def access():
	'''
	To access the value of the global variable
	'''
	with open("var.txt", "r+") as f:
		line = f.read()

	var = int(line)
	return var
