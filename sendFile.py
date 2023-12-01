import paramiko
import os
import schedule
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

    for filename in os.listdir(local_directory):
        local_path = os.path.join(local_directory, filename)

        if os.path.isfile(local_path) and not file_already_exists(ssh_client, remote_directory, filename):
            new_files_found = True
            print(f"Copying {filename} to remote directory...")
            ssh_client.put(local_path, os.path.join(remote_directory, filename))
            print(f"{filename} successfully copied.")
        else:
            print(f"Skipped {filename}, already exists in remote directory.")

    return new_files_found

def job():
    print("Job started.")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("SSH client setup complete.")

    # Replace with your details
    host = "denver.cs.colostate.edu"
    port = 22
    username = "rblocker"
    password = "RCB+thecsbuilding"

    try:
        print(f"Attempting to connect to {host}...")
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        print("SSH connection established.")
        sftp = ssh_client.open_sftp()

        # Define your source and target directories
        local_directory = '/Users/ryanblocker/fileBackup'
        remote_directory = '/s/bach/j/rblocker/fileBackup'

        if not copy_files_to_remote(sftp, local_directory, remote_directory):
            print("No new files to copy. Stopping the program.")
            return

        print("File transfer complete.")

    except Exception as e:
        print(f"Connection Failed: {e}")
    finally:
        ssh_client.close()
        print("SSH client closed.")

# Schedule the job every hour
schedule.every().second.do(job)
print("Job scheduled to run every hour.")

while True:
    schedule.run_pending()
    time.sleep(1)
