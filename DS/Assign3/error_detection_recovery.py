import hashlib
import json
import account as acc
import log_handling as logh

def check_log_consistency(pid=None):
	'''
	Check whether any deamon process has corrupted it's log file by comparing their hash value
	'''
	
	checkpoint = "./server/stable_storage/checkpoints/"
	log = "./server/local_storage/client_log/"

	if pid is None:
		all_process = acc.all_process()
		consistent, deamon = True, []

		for pid, _ in all_process:
			path = checkpoint + str(pid) + "/"

			with open(path + "checkpoint.txt", "r") as fc:
				last_saved = fc.read()

			with open(path + "changes.txt", "r") as fc:
				change = fc.read()

			data_saved = last_saved + change

			with open(log + str(pid) + "/log.txt", "r") as fl:
				data_cur = fl.read()

			hash_saved = hashlib.sha256(data_saved.encode()).hexdigest()
			hash_cur = hashlib.sha256(data_cur.encode()).hexdigest()

			if hash_cur != hash_saved:
				# print(data_cur)
				# print(data_saved)
				# print(pid)
				consistent = False
				deamon.append(pid)
				acc.block(pid)


	return consistent, deamon


def create_checkpoint(cur_time):
	'''
	Save the current state of log files of all processes into a stable, and more reliable storeage (secondary storage)
	'''

	all_process = acc.all_process()
	log_path = "./server/local_storage/client_log/"
	checkpoint_path = "./server/stable_storage/checkpoints/"

	for pid, _ in all_process:
		log_file_path = log_path + str(pid) + "/log.txt"
		checkpoint_file_path = checkpoint_path + str(pid) + "/"

		with open(log_file_path, "r") as fr:
			content = fr.read()

		with open(checkpoint_file_path + "checkpoint.txt", "w")as fw:
			fw.write(content)

		with open(checkpoint_file_path + "changes.txt", "w") as fw:
			fw.write("")

		with open(checkpoint_path + "timestamps.txt", "a+") as fa:
			fa.write(cur_time + "\n")

	new_log = json.dumps({
		"TYPE": "CHECKPOINT",
		"TIMESTAMP": cur_time,
		"STATUS": "SUCCESS"
	})

	logh.create_new_log(None, new_log, write=False, change=False, server=True)

	print(" --------------------")
	print("| CHECKPOINT CREATED |")
	print(" --------------------")


def revert_back_changes(all_process, cur_time):
	'''
	Revert back all the changes made since last checkpoint has been created
	'''

	checkpoint_path = "./server/stable_storage/checkpoints/"

	for pid, active_status in all_process:
		changes = checkpoint_path + str(pid) + "/changes.txt"

		with open(changes, "r") as fr:
			while True:
				log = fr.readline()

				if log:
					l = json.loads(log)
					if l["TYPE"] == "DEBIT" and l["STATUS"] == "SUCCESS":
						debit, credit, amount = l["FROM"], l["TO"], l["AMOUNT"]

						debit_notification = "[ " + cur_time + " ] : $" + str(amount) + " recovered from your account and credited to " + debit + " [ SYSTEM RECOVERY ]"
						credit_notification = "[ " + cur_time + " ] : $" + str(amount) + " credited to your account, recovered from " + credit + " [ SYSTEM RECOVERY ]"

						logh.create_notification(debit, credit_notification, 'N')
						logh.create_notification(credit, debit_notification, 'N')

				else:
					break


def backward_error_recovery(cur_time):
	'''
	Recover from current erroneous state by rolling back to the previous saved checkpoint
	'''

	all_process = acc.all_process()
	log_path = "./server/local_storage/client_log/"
	checkpoint_path = "./server/stable_storage/checkpoints/"

	for pid, _ in all_process:
		# Retrieve log data from last saved checkpoint
		log_file_path = log_path + str(pid) + "/log.txt"
		checkpoint_file_path = checkpoint_path + str(pid) + "/"
		
		with open(checkpoint_file_path + "checkpoint.txt", "r")as fr:
			content = fr.read()

		with open(log_file_path, "w") as fw:
			fw.write(content)

		# Revert back all the changes
		revert_back_changes(all_process, cur_time)

		create_checkpoint(cur_time)

		with open(checkpoint_file_path + "changes.txt", "w") as fw:
			fw.write("")

		# with open(checkpoint_path + "timestamps.txt", "a+") as fa:
		# 	fa.write(cur_time + "\n")

	new_log = json.dumps({
		"TYPE": "BER",
		"TIMESTAMP": cur_time,
		"STATUS": "SUCCESS"
	})

	logh.create_new_log(None, new_log, write=False, change=False, server=True)

	print(" ------------------")
	print("| SYSTEM RECOVERED |")
	print(" ------------------")

if __name__ == '__main__':
	print(check_log_consistency())