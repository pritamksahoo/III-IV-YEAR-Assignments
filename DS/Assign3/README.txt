Directory structure:

Assign3
    |___server/
    |      |___local_storage/
           |        |___client_log/
    |      |
    |      |___stable_storage/
    |                |___accounts/
    |                |       |___accounts.csv
    |                |
    |                |___checkpoints/
    |                |       |___timestamps.txt
    |                |
    |                |__notifications/
    |
    |___server.py
    |
    |___client.py
    |
    |___account.py :: Handles signup, login, logout, etc.
    |
    |___log_handling.py :: Handle all logs and notifications
    |
    |___error_detection_recovery.py :: Detect error and recovery


1) New account (pid, password) creation creates - 
    i]accounts/
        |___accounts.csv :: Append new client record 

    ii]client_log/
            |___<pid>/
                  |___log.txt :: Logs are saved here, accessible to client

    iii]checkpoints/
            |___<pid>/
                  |___checkpoint.txt :: Checkpoint, accessible to only server
                  |___changes.txt :: Changes made since last checkpoint, same
                  
    iv]notifications
            |___<pid>/
                  |___notifications.csv :: All notifications

2) Client can -
    i] Make transactions [DEBIT, FROM: <own_pid>, TO: <some_pid>]

        --- Clients have to specify the credit PID and AMOUNT

    ii] Access its log records [Deamon process make changes in log records before giving back to server, leading to inconsistency]

        --- Clients have to provide a directory path (with a "/" at the end) where logs will be fetched (will be saved in a file "log.txt" in that directory, so clients don't need to mention any filename).

        --- Then the file has to be returned. Client can change the file content before sending it back. That client will be detected as a deamon process by the server later.

        --- If any transaction takes place between log corruption and next recent background consistency check, those will be reverted back during rolling out to the last safe state.

    iii] Log Out

3) Server -
    i] Handle client requests

    ii] Run a background check for consistency at a regular time interval

4) RUN - 
    i] python3 server.py

    ii] Multiple python3 client.py

    iii] ENJOY!