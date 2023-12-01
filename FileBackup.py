import paramiko
import os
import time


def file_already_exists(sftp, remote_directory, filename):
    try:
        sftp.stat(os.path.join(remote_directory, filename))
        return True
    except IOError:
        return False

def copy_files_to_remote(ssh_client, local_directory, remote_directory):
    print("Starting to copy files...")
    new_files_found = False

    for filename in os.listdir(remote_directory):
        remote_path = os.path.join(remote_directory, filename)

        if os.path.isfile(remote_path) and not file_already_exists(ssh_client, local_directory, filename):
            new_files_found = True
            print(f"Copying {filename} to local directory...")
            ssh_client.put(remote_path, os.path.join(local_directory, filename))
            print(f"{filename} successfully copied.")
        else:
            print(f"Skipped {filename}, already exists in local directory.")

    return new_files_found


    
def ssh():
    print("Job started.")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("SSH client setup complete.")

    # Replace with your details
    host = "dragonfly.cs.colostate.edu"
    port = 22
    username = "emmars"
    password = "dexter1234554321"

    try:
        print(f"Attempting to connect to {host}...")
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        print("SSH connection established.")
        sftp = ssh_client.open_sftp()

        # Define your source and target directories
        remote_directory = 'BackupFiles/'
        local_directory = '/Users/emmashneidman/BackupFiles'
        
        _stdin, _stdout,_stderr = ssh_client.exec_command(f"cd {remote_directory} \n ls")
        print(_stdout.read().decode())

        if not copy_files_to_remote(sftp, local_directory, remote_directory):
            print("No new files to copy. Stopping the program.")
            return

        print("File transfer complete.")

    except Exception as e:
        print(f"Connection Failed: {e}")
    finally:
        ssh_client.close()
        print("SSH client closed.")
        
    
    
if __name__ == "__main__":
    print("hello")
    ssh()
    