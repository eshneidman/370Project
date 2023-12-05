import paramiko
import os
import schedule
import time

copy_to_remote = []
copied_to_remote = []

remote_directory = '/s/bach/l/under/emmars/BackupFiles/'
local_directory = '/Users/emmashneidman/BackupFiles/'

def copy():
    # Connect to client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname = 'moscow.cs.colostate.edu', username='emmars', password='dexter1234554321')
    sftp_client = ssh_client.open_sftp()
    
    #Change directory to BackupFiles folder
    sftp_client.chdir(remote_directory)
    files = sftp_client.listdir(remote_directory)
    
    #Copy files from remote directory to local directory
    for file in files:
        remote_file_path = os.path.join(remote_directory, file)
        local_file_path = os.path.join(local_directory, file)
        sftp_client.get(remote_file_path, local_file_path)

    ssh_client.close()
    


def get_new_files(local_directory, copy_to_remote, copied_to_remote):
    #Loop through files in local directory
    all_files = [f for f in os.listdir(local_directory) if os.path.isfile(os.path.join(local_directory, f))]
    
    for file in all_files:
        if file not in copied_to_remote:
            copy_to_remote.append(file)
            
    print(copy_to_remote[0])
    
def job():
    
    #Copy from remote
    copy()
    
    #Get files from local
    get_new_files(local_directory, copy_to_remote, copied_to_remote)
    
    #Connect to client 
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='dragonfly.cs.colostate.edu', username='rblocker', password='RCB+thecsbuilding')
    sftp_client = ssh_client.open_sftp()

    #Copy files from local to remote
    for file in copy_to_remote:
        local_file_path = os.path.join(local_directory, file)
        remote_file_path = '/s/bach/j/under/rblocker/fileBackup/' + file
        sftp_client.put(local_file_path, remote_file_path)
        copy_to_remote.remove(file)
        copied_to_remote.append(file)
        if not copy_to_remote:
            print("Transfer complete")
            exit()
    
    sftp_client.close()
    ssh_client.close()
    
    
def main():
    print("Starting backup")
    
    schedule.every().second.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

    
if __name__ == "__main__":
    main()
    
        
    
    
    
    
    