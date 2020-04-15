def check_log_consistency(pid=None):
    '''
    Check whether any deamon process has corrupted it's log file by comparing their hash value
    '''
    
    return False, ['abcde']


def create_checkpoint():
    '''
    Save the current state of log files of all processes into a stable, and more reliable storeage (secondary storage)
    '''

    pass


def backward_error_recovery():
    '''
    Recover from current erroneous state by rolling back to the previous saved checkpoint
    '''

    pass