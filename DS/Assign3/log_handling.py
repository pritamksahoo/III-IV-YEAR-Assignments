import os
import pandas as pd
import json
import hashlib
import account as acc
from server import cur_time as t_now

def create_directory(parent, directory, files=None):
	'''
	Create new directory in specified path and create new files inside that directory(optional)
	'''

	new_dir_path = os.path.join(parent, directory)
	os.mkdir(new_dir_path)

	# Create optional files in the newly created directory
	if files is not None:
		for file in files:
			with open(new_dir_path + "/" + file, "w") as f:
				pass


def create_new_log_file(pid):
	'''
	Creating necessary log files corresponding to newly created account
	'''
	# Primary log files, accessible to client
	client_log_path = "./server/local_storage/client_log/"
	create_directory(client_log_path, str(pid), ['log.txt'])

	# Secondary notification files, not accessible to client
	client_note_path = "./server/stable_storage/notifications/"
	create_directory(client_note_path, str(pid), ['notifications.csv'])

	# For creating checkpoints, not accessible to client
	checkpoint_path = "./server/stable_storage/checkpoints/"
	create_directory(checkpoint_path, str(pid), ['checkpoint.txt', 'changes.txt'])


def create_new_log(pid, log_data, write=True, change=True, server=False):
	'''
	Create a new line of log into a process's log file
	'''

	log_path = "./server/local_storage/client_log/" + str(pid) + "/log.txt"
	checkpoint_path = "./server/stable_storage/checkpoints/" + str(pid) + "/changes.txt"
	server_log_path = "./server/stable_storage/server_log/log.txt"

	if acc.is_active(pid) is None:
		# No such process (online / offline) exists
		return False

	try:
		if pid is not None:
			# Write in client's log
			with open(log_path, "a+") as fw:
				if write:
					fw.write(log_data + "\n")

			with open(checkpoint_path, "a+") as fw:
				if write and change:
					fw.write(log_data + "\n")

		# Append in server log
		with open(server_log_path, "a+") as fs:
			if server:
				fs.write(log_data + "\n")

		return True

	except Exception as e:
		# print(e)
		s_log = json.dumps({
			"TYPE": "ERROR",
			"ERROR_DOMAIN": "CREATE_NEW_LOG",
			"TIMESTAMP": t_now(),
			"ERROR_DESC": str(e)
		})
		create_new_log(None, s_log, False, False, True)

		return False


def fetch_client_log(pid):
	'''
	Fetch log for the process with given pid. Hash is created of the log for integrity check
	'''

	client_log = []

	try:
		log_path = "./server/local_storage/client_log/" + str(pid) + "/log.txt"
		f = open(log_path, "rb")
		
		# Reading the client log with given pid by a chunk of 1024 B
		log = f.read(1024)
		while log:
			client_log.append(log)
			log = f.read(1024)

		f.close()

	except Exception as e:
		s_log = json.dumps({
			"TYPE": "ERROR",
			"ERROR_DOMAIN": "FETCH_CLIENT_LOG",
			"TIMESTAMP": t_now(),
			"ERROR_DESC": str(e)
		})
		create_new_log(None, s_log, False, False, True)

	return client_log


def create_notification(pid, message, status):
	'''
	Create a new notification for a process and send it if the process is still active, otherwise it is sent after process comes alive again
	'''

	client_note_file = "./server/stable_storage/notifications/" + str(pid) + "/notifications.csv"

	try:
		# Appending to the notification.csv file
		new_notification = {"message": message, "read": status}
		notifications = pd.read_csv(client_note_file)
		notifications = notifications.append(new_notification, ignore_index=True)

	except Exception as e:
		# Creating first notification for a client
		new_notification = {"message": [message], "read": [status]}
		notifications = pd.DataFrame(new_notification)

	notifications.to_csv(client_note_file, index=False, header=True)


def retrieve_unread_notifications(pid):
	'''
	Fetch all unread notifications for a process
	'''

	client_note_file = "./server/stable_storage/notifications/" + str(pid) + "/notifications.csv"

	try:
		notifications = pd.read_csv(client_note_file)

		unread = notifications.loc[notifications['read'] == 'N']
		index = notifications.index[notifications['read'] == 'N'].tolist()
		unread_notifications = unread['message'].to_list()

		# Marking messages read
		for ind in index:
			notifications.at[ind, 'read'] = 'Y'

		notifications.to_csv(client_note_file, index=False, header=True)

	except Exception as e:
		# print(e)
		s_log = json.dumps({
			"TYPE": "ERROR",
			"ERROR_DOMAIN": "FETCH_UNREAD_NOTIFICATIONS",
			"TIMESTAMP": t_now(),
			"ERROR_DESC": str(e)
		})
		create_new_log(None, s_log, False, False, True)

		unread_notifications = []

	return unread_notifications


def send_notifications_to_clients(pid):
	'''
	Retrieve all notifications of an active process and send all unread notifications to it
	'''

	status = acc.is_active(pid)

	if status is None:
		return None
	elif status:
		note = retrieve_unread_notifications(pid)
		return note
	else:
		return [None]


if __name__ == '__main__':
	print(retrieve_unread_notifications("pritam"))