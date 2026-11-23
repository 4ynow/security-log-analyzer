import time 
import json
import re
import requests
import os

SERVER_URL = "http://127.0.0.1:8080/server/ingest.php"
API_KEY = "key123"
LOG_FILE = "/var/log/auth.log"

def send_log():
    payload = {
        "agent_id": "kali-vm",
        "message": "test connection",
        "source": "linux-auth",
        "event_type": "test",
        "source_ip": "1.2.3.4",
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
        
if __name__ == "__main__":
    send_log()
