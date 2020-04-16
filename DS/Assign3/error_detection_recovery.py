import hashlib
import account as acc

def check_log_consistency(pid=None):
    '''
    Check whether any deamon process has corrupted it's log file by comparing their hash value
    '''
    
    checkpoint = "./server/stable_storage/checkpionts/"
    log = "./server/local_storage/client_log/"

    if not pid:
        all_process = acc.all_process()
        isConsistent, deamon = True, []

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
                isConsistent = False
                deamon.append(pid)


    return isConsistent, deamon


def create_checkpoint():
    '''
    Save the current state of log files of all processes into a stable, and more reliable storeage (secondary storage)
    '''

    all_process = acc.all_process()
    log_path = "./server/local_storage/client_log/"
    checkpoint_path = "./server/stable_storage/checkpoints/"

    for pid, _ in all_process:
        log_file_path = log_path + str(pid) + "/"
        checkpoint_file_path = checkpoint_path + str(pid) + "/"
        
    pass


def backward_error_recovery():
    '''
    Recover from current erroneous state by rolling back to the previous saved checkpoint
    '''

    pass