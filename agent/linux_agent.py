import time 
import re
import requests
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
        "severity": "medium"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        "User-Agent": "LogSec-Agent/1.0",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(SERVER_URL, headers=headers, json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"[+] Sent log: {username} from {ip}")
        else:
            print(f"[-] Error: {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error, could not reach server: {e}")

def tail_file(filepath):
    try:
        with open(filepath, "r") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                
                process_line(line)
                
    except FileNotFoundError:
        print(f"[!] Error: The file {filepath} does not exist.")
    except PermissionError:
        print(f"[!] Error: Permission denied. Run the agent with sudo.")
    except Exception as e:
        print(f"[!] Unexpected error reading file: {e}")
        
def process_line(line):
    pattern = r"Failed password for (?:invalid user )?(\S+) from (\S+)"
    match = re.search(pattern, line)
    
    if match:
        username = match.group(1)
        ip = match.group(2)
        raw_line = line.strip()
        
        send_log(username, ip, raw_line)

if __name__ == "__main__":
    print(f"[*] Watching {LOG_FILE}...")
    try:
        tail_file(LOG_FILE)
    except KeyboardInterrupt:
        print("\n[*] Agent stopped.")
