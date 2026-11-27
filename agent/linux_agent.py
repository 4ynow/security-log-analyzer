import time 
import re
import requests
import socket

SERVER_URL = "http://127.0.0.1:8080/server/ingest.php"
API_KEY = "key123"
LOG_FILE = "/var/log/auth.log"

AUTH_RULES = [
    {
        "pattern": r"Failed password for (?:invalid user )?(\S+) from (\S+)",
        "event_type": "ssh_failed",
        "severity": "medium"
    },
    {
        "pattern": r"Accepted password for (\S+) from (\S+)",
        "event_type": "ssh_success",
        "severity": "info"
    },
    {
        "pattern": r"sudo:\s+(\S+)\s+:.*COMMAND=(.*)",
        "event_type": "sudo_command",
        "severity": "high"
    }
]

def send_log(username, ip, raw_line, event_type, severity):
    payload = {
        "agent_id": socket.gethostname(),
        "username": username,
        "message": raw_line,
        "source": "linux-auth",
        "event_type": event_type,
        "source_ip": ip,
        "severity": severity
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
            print(f"[+] Sent {event_type}: {username} from {ip}")
        else:
            print(f"[-] Error: {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error, could not reach server: {e}")

def tail_file(filepath, rule_set):
    try:
        with open(filepath, "r") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                
                process_line(line, rule_set)
                
    except FileNotFoundError:
        print(f"[!] Error: The file {filepath} does not exist.")
    except PermissionError:
        print(f"[!] Error: Permission denied. Run the agent with sudo.")
    except Exception as e:
        print(f"[!] Unexpected error reading file: {e}")
        
def process_line(line, rule_set):
    for rule in rule_set:
        match = re.search(rule["pattern"], line)
        
        if match:
            username = match.group(1)
            
            if len(match.groups()) > 1:
                ip = match.group(2)
            else:
                ip = "localhost"
                
            send_log(username, ip, line.strip(), rule["event_type"], rule["severity"])
            break

if __name__ == "__main__":
    print(f"[*] Watching {LOG_FILE}...")
    try:
        tail_file(LOG_FILE, AUTH_RULES)
    except KeyboardInterrupt:
        print("\n[*] Agent stopped.")
