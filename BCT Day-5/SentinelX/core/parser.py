import time
from scapy.all import Packet, IP, TCP, UDP, ICMP, ARP, DNS

def parse_packet(packet: Packet) -> dict:
    """Parses a Scapy packet into a unified dictionary structure."""
    parsed = {
        "timestamp": time.time(),
        "time_str": time.strftime("%H:%M:%S", time.localtime()),
        "src_ip": None,
        "dst_ip": None,
        "src_port": None,
        "dst_port": None,
        "protocol": "UNKNOWN",
        "flags": "",
        "length": len(packet),
        "ttl": None,
        "payload_size": 0,
        "mac_src": None,
        "mac_dst": None,
        "raw_payload": ""
    }

    if packet.haslayer('Ether'):
        parsed["mac_src"] = packet['Ether'].src
        parsed["mac_dst"] = packet['Ether'].dst

    if packet.haslayer(IP):
        parsed["src_ip"] = packet[IP].src
        parsed["dst_ip"] = packet[IP].dst
        parsed["ttl"] = packet[IP].ttl
        
        if packet.haslayer(TCP):
            parsed["protocol"] = "TCP"
            parsed["src_port"] = packet[TCP].sport
            parsed["dst_port"] = packet[TCP].dport
            parsed["flags"] = packet[TCP].flags
            parsed["raw_payload"] = bytes(packet[TCP].payload).hex()
            parsed["payload_size"] = len(parsed["raw_payload"])
            
            # Simple HTTP/SSH check based on port and payload
            if parsed["dst_port"] == 80 or parsed["src_port"] == 80:
                parsed["protocol"] = "HTTP"
            elif parsed["dst_port"] == 22 or parsed["src_port"] == 22:
                parsed["protocol"] = "SSH"
            elif parsed["dst_port"] == 21 or parsed["src_port"] == 21:
                parsed["protocol"] = "FTP"

        elif packet.haslayer(UDP):
            parsed["protocol"] = "UDP"
            parsed["src_port"] = packet[UDP].sport
            parsed["dst_port"] = packet[UDP].dport
            parsed["raw_payload"] = bytes(packet[UDP].payload).hex()
            parsed["payload_size"] = len(parsed["raw_payload"])
            
            if packet.haslayer(DNS):
                parsed["protocol"] = "DNS"
                
        elif packet.haslayer(ICMP):
            parsed["protocol"] = "ICMP"
            parsed["raw_payload"] = bytes(packet[ICMP].payload).hex()
            parsed["payload_size"] = len(parsed["raw_payload"])
            
    elif packet.haslayer(ARP):
        parsed["protocol"] = "ARP"
        parsed["src_ip"] = packet[ARP].psrc
        parsed["dst_ip"] = packet[ARP].pdst

    return parsed
