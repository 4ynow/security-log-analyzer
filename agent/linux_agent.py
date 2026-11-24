import time 
import json
import re
import requests
import os
import socket

SERVER_URL = "http://127.0.0.1:8080/server/ingest.php"
API_KEY = "key123"
LOG_FILE = "/var/log/auth.log"

def send_log(username, ip, raw_line):
    
    payload = {
        "agent_id": socket.gethostname(),
        "username": username,
        "message": raw_line,
        "source": "linux-auth",
        "event_type": "ssh_failed",
        "source_ip": ip,
        "severity": "info"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "key123",
        "User-Agent": "LogSec-Agent/1.0",
        "Accept": "application/json"
    }
    
    response = requests.post(SERVER_URL, headers=headers, json=payload)
    
    
    
    if response.status_code == 200:
        print("[+] Success; Server received the log.")
    else:
        print(f"[-] Error: {response.status_code}: {response.text}")
        
def tail_file(filepath):
    with open(filepath, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            process_line(line)
        
def process_line(line):
    pattern =pattern = r"Failed password for (?:invalid user )?(\S+) from (\S+)"
    match = re.search(pattern, line)
    
    if match:
        username = match.group(1)
        ip = match.group(2)
        raw_line = line.strip()
        
        send_log(username, ip, raw_line)


        
if __name__ == "__main__":
    print("[*] Watching the log file...")
    try:
        tail_file(LOG_FILE)
    except KeyboardInterrupt:
        print("\n[*] Agent stopped.")
