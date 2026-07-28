import argparse
import time
from scapy.all import IP, TCP, send

parser = argparse.ArgumentParser(description="SentinelX - Port Scan Simulator")
parser.add_argument("--target", required=True, help="Target IP address")
parser.add_argument("--delay", type=float, default=0.01, help="Delay between packets")
args = parser.parse_args()

print(f"[*] Starting Port Scan against {args.target}")
print(f"[*] Scanning ports 1 to 1024 with {args.delay}s delay...")

try:
    sent = 0
    for port in range(1, 1025):
        packet = IP(dst=args.target)/TCP(dport=port, flags="S")
        send(packet, verbose=0)
        sent += 1
        if args.delay > 0:
            time.sleep(args.delay)
    print(f"\n[+] Port scan completed. Scanned {sent} ports.")
except KeyboardInterrupt:
    print(f"\n[!] Scan aborted by user. Scanned {sent} ports.")
except Exception as e:
    print(f"\n[!] Error: {e}")
