import os
import pandas as pd
import json
import account as acc

def create_directory(parent, directory, files=None):
    '''
    Create new directory in specified path and create new files inside that directory(optional)
    '''

    new_dir_path = os.path.join(parent, directory)
    os.mkdir(new_dir_path)

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


def create_new_log(pid, log_data):
    '''
    Create a new line of log into a process's log
    '''

    log_path = "./server/local_storage/client_log/" + str(pid) + "/log.txt"

    with open(log_path, "a+") as fw:
        fw.write(json.dumps(log_data) + "\n")


def check_log_consistency(pid=None):
    '''
    Check whether any deamon process has corrupted it's log file by comparing their hash value
    '''
    
    pass


def create_checkpoint():
    '''
    Save the current state of log files of all processes into a stable, and more reliable storeage (secondary storage)
    '''

    pass



def create_notification(pid, message, status):
    '''
    Create a new notification for a process and send it if the process is still active, otherwise it is sent after process comes alive again
    '''

    client_note_file = "./server/stable_storage/notifications/" + str(pid) + "/notifications.csv"

    try:
        new_notification = {"message": message, "read": status}
        notifications = pd.read_csv(client_note_file)
        notifications = notifications.append(new_notification, ignore_index=True)

    except Exception as e:
        new_notification = {"message": [message], "read": [status]}
        notifications = pd.DataFrame(new_notification)

    notifications.to_csv(client_note_file, index=False, header=True)


def retrieve_unread_notifications(pid):
    '''
    Fetch all unread notifications for a process
    '''

    client_note_file = "./server/local_storage/client_log/" + str(pid) + "/notifications.csv"

    try:
        notifications = pd.read_csv(client_note_file)
        unread = notifications.loc[notifications['read'] == 'N']
        index = notifications.index[notifications['read'] == 'N'].tolist()
        unread_notifiactions = unread['message']

        # Marking messages read
        for ind in index:
            notifications.at[ind, 'read'] = 'Y'

        notifications.to_csv(client_note_file, index=False, header=True)

    except Exception as e:
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
        return retrieve_unread_notifications(pid)
    else:
        return [None]