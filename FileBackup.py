import paramiko
import os
import time

def ssh():
    
    host = "desmoines.cs.colostate.edu"
    port = 22
    username = "emmars"
    password = "dexter1234554321"

    
    try:
        client = paramiko.SSHClient()
        
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,port,username,password)
        
        print(f"SUCCESS connected to {host}")
        return client
    except Exception as e:
        print(f"FAILED {e}")
        return None
    
    
if __name__ == "__main__":
    print("hello")
    ssh()
    