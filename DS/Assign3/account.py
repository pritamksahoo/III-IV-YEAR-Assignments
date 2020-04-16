import pandas as pd
import log_handling as logh


def is_active(pid):
	'''
	Check whether a process is still active
	'''

	filepath = "./server/stable_storage/accounts/accounts.csv"
	accounts = pd.read_csv(filepath)

	record = accounts.loc[accounts['pid'] == pid]

	if record.empty:
		# Wrong PID
		return None
	elif record["isActive"].to_list()[0] == 'B':
		# Blocked account
		return None
	elif record["isActive"].to_list()[0] == 'Y':
		# Active
		return True
	else:
		# Logged Out
		return False


def all_process():
	'''
	Fetch PID and active status of all process
	'''

	filepath = "./server/stable_storage/accounts/accounts.csv"
	accounts = pd.read_csv(filepath)

	pid, active_status = accounts["pid"].to_list(), accounts["isActive"].to_list()

	return [(pid[i], active_status[i]) for i in range(len(pid))]


def create_account(pid, password, addr, cur_time):
	'''
	Creates an account with unique pid and password and variable address (hostname and port). Address can change every time client shuts down and restarts again. Throws error if pid already exists
	'''

	filepath = "./server/stable_storage/accounts/accounts.csv"
	accounts = pd.read_csv(filepath)

	hostname, port = addr
	record = accounts.loc[accounts['pid'] == pid]
	# print(record.empty)

	if record.empty:
		active_status = 'N'
		new_record = {
			'pid': pid,
			'password': password,
			'host': hostname,
			'port': port,
			'isActive': active_status
		}

		accounts = accounts.append(new_record, ignore_index=True)

		try:
			# Creating new account
			accounts.to_csv(filepath, index=False, header=True)
			logh.create_new_log_file(pid)

			status = 200
			message = "[ " + cur_time + " ] : Account successfully created"

			logh.create_notification(pid, message, 'Y')

		except Exception as e:
			status = 400
			message = "[ " + cur_time + " ] : Account creation failed! Server Error! Try again later"

	else:
		status = 400
		message = "[ " + cur_time + " ] : Account creation failed! PID already exists"

	data = {
		"status": status,
		"message": message
	}

	return data


def login(pid, password, addr, cur_time):
	'''
	Log in to a client's acount, address my be different after restart. So, it's need to be updated
	'''

	filepath = "./server/stable_storage/accounts/accounts.csv"
	accounts = pd.read_csv(filepath)

	record = accounts.loc[(accounts['pid'] == pid) & (accounts['password'] == password)]
	# print(record["isActive"].to_list())

	if not record.empty and record["isActive"].to_list()[0] == 'Y':
		status = 400
		message = "[ " + cur_time + " ] : Login Failed! Already running in another window"

	elif not record.empty and record["isActive"].to_list()[0] == 'B':
		status = 400
		message = "[ " + cur_time + " ] : Login Failed! Account is blocked"    
	
	elif not record.empty:
		hostname, port = addr

		# Updating address
		index = accounts.index[(accounts['pid'] == pid) & (accounts['password'] == password)].tolist()[0]
		accounts.at[index, 'host'] = hostname
		accounts.at[index, 'port'] = port
		accounts.at[index, 'isActive'] = 'Y'
		accounts.to_csv(filepath, index=False, header=True)

		status = 200
		message = "[ " + cur_time + " ] : You are logged in"
		
		logh.create_notification(pid, message, 'Y')

	else:
		status = 400
		message = "[ " + cur_time + " ] : Login Failed! Wrong PID or PASSWORD"

	data = {
		"status": status,
		"message": message
	}

	return data    


def logout(pid, cur_time):
	'''
	Client logged out of the system
	'''

	filepath = "./server/stable_storage/accounts/accounts.csv"
	accounts = pd.read_csv(filepath)

	index = accounts.index[accounts["pid"] == pid].to_list()[0]
	if accounts.at[index, "isActive"] == 'Y':
		accounts.at[index, "isActive"] = 'N'

		message = "[ " + cur_time + " ] : You are logged out"
		logh.create_notification(pid, message, 'Y')

		accounts.to_csv(filepath, index=False, header=True)


def block(pid):
	'''
	Client blocked the system
	'''

	filepath = "./server/stable_storage/accounts/accounts.csv"
	accounts = pd.read_csv(filepath)

	index = accounts.index[accounts["pid"] == pid].to_list()[0]
	accounts.at[index, "isActive"] = 'B'

	accounts.to_csv(filepath, index=False, header=True)


if __name__ == '__main__':
	# print(login("abcde", "pass", ['127.0.0.1', 8800]))
	# logh.create_new_log("abcde", {"from": "a", "to": "b", "amount": 100})
	print(all_process())