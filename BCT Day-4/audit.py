import requests
import time
import sys

LOGIN_URL = 'http://localhost:5000/login'
DASHBOARD_URL = 'http://localhost:5000/dashboard'

def load_list(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        sys.exit(1)

def run_audit():
    print("========================================")
    print("SECURITY AUDIT: Starting Brute Force Test")
    print("========================================\n")
    
    usernames = load_list('usernames.txt')
    passwords = load_list('passwords.txt')
    
    # We will test a subset of combinations to demonstrate the attack
    # For a real brute force, this might be a nested loop. Here we'll
    # just pair them up, but also test a few invalid passwords for a user
    # to trigger the lockout mechanism.
    
    # Let's specifically target 'admin' to show lockout
    target_user = 'admin'
    print(f"[*] Targeting user: {target_user}")
    
    vulnerabilities = []
    
    # Send multiple requests with wrong passwords to trigger lockout
    print("\n[!] Phase 1: Testing Account Lockout Mechanism")
    for i in range(7):
        password_guess = f"wrongpass{i}"
        print(f"[*] Attempting {target_user} : {password_guess} ...", end=" ")
        
        # We need a session to persist cookies, just like a real browser
        session = requests.Session()
        data = {'username': target_user, 'password': password_guess}
        
        response = session.post(LOGIN_URL, data=data)
        
        if "Account locked" in response.text:
            print("BLOCKED (Account Lockout Triggered!)")
        elif "Invalid username or password" in response.text:
            print("FAILED")
        elif response.status_code == 429:
            print("BLOCKED (Rate Limited by IP!)")
        else:
            print("UNKNOWN RESPONSE")
            
        time.sleep(0.5)
        
    print("\n[!] Phase 2: Testing Valid Credentials Pairing")
    # Now pair up some valid ones to see if rate limiting catches us
    for i in range(min(15, len(usernames))):
        user = usernames[i]
        password = passwords[i]
        
        print(f"[*] Attempting {user} : {password} ...", end=" ")
        
        session = requests.Session()
        data = {'username': user, 'password': password}
        
        response = session.post(LOGIN_URL, data=data)
        
        if response.status_code == 429:
            print("BLOCKED (Rate Limited by IP!)")
            continue
            
        if "Account locked" in response.text:
            print("BLOCKED (Account Lockout)")
            continue
            
        # Check if login was successful (redirected to dashboard or session established)
        if response.url == DASHBOARD_URL or "Welcome," in response.text:
            print("SUCCESS - VULNERABILITY FOUND!")
            vulnerabilities.append((user, password))
        else:
            print("FAILED")
            
        # Optional: slight delay to simulate script speed
        time.sleep(0.2)
        
    print("\n========================================")
    print("AUDIT COMPLETE")
    print("========================================")
    print(f"Total Vulnerabilities Found: {len(vulnerabilities)}")
    for vuln in vulnerabilities:
        print(f" - Valid Credential: {vuln[0]} / {vuln[1]}")

if __name__ == '__main__':
    run_audit()
