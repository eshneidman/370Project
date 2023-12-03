import paramiko
import os
import schedule
import time

copy_to_remote = []
copied_to_remote = []

local_directory = '/Users/ryanblocker/fileBackup'

def get_new_files(local_directory, copy_to_remote, copied_to_remote):
    all_files = [f for f in os.listdir(local_directory) if os.path.isfile(os.path.join(local_directory, f))]
    
    for file in all_files:
        if file not in copied_to_remote:
            copy_to_remote.append(file)
            
    print(copy_to_remote)
    
def job():
    
    get_new_files(local_directory, copy_to_remote, copied_to_remote)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='moscow.cs.colostate.edu', username='rblocker', password='RCB+thecsbuilding')
    sftp_client = ssh_client.open_sftp()

    for file in copy_to_remote:
        local_file_path = os.path.join(local_directory, file)
        remote_file_path = '/s/bach/j/under/rblocker/fileBackup/' + file
        sftp_client.put(local_file_path, remote_file_path)
        copy_to_remote.remove(file)
        copied_to_remote.append(file)
    
    sftp_client.close()
    ssh_client.close()
    
    
def main():
    print("process start")
    
    schedule.every().hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
    
    
if __name__ == "__main__":
    main()
    
        
    
    
    
    
    