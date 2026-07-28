import threading
import time
from queue import Queue, Empty
from collections import defaultdict
from core.parser import parse_packet
from core.logger import log_alert, log_packet_json
from rules.rule_engine import RuleEngine

class DetectionEngine:
    def __init__(self, packet_queue: Queue, rule_engine: RuleEngine):
        self.packet_queue = packet_queue
        self.rule_engine = rule_engine
        self.running = False
        self.thread = None
        
        # Stats for the dashboard
        self.stats = {
            "total_packets": 0,
            "dropped_packets": 0,
            "alerts_generated": 0,
            "protocols": defaultdict(int),
            "top_src": defaultdict(int),
            "top_dst": defaultdict(int),
            "top_ports": defaultdict(int)
        }
        
        # Sliding windows: {src_ip: [timestamp1, timestamp2, ...]}
        self.windows = {
            "ICMP": defaultdict(list),
            "SYN": defaultdict(list),
            "UDP": defaultdict(list),
            "DNS": defaultdict(list),
            "SSH": defaultdict(list),
            "PORTS": defaultdict(set) # For port scans: {src_ip: set((port, timestamp))}
        }
        
        self.recent_alerts = [] # List of tuples (severity, rule, src_ip, timestamp)

    def _clean_window(self, window_list, current_time, window_size):
        """Removes timestamps older than (current_time - window_size)"""
        # Keep only timestamps within the window
        return [ts for ts in window_list if current_time - ts <= window_size]

    def _clean_port_window(self, port_set, current_time, window_size):
        return {item for item in port_set if current_time - item[1] <= window_size}

    def _process(self):
        while self.running:
            try:
                packet = self.packet_queue.get(timeout=1.0)
                parsed = parse_packet(packet)
                self.stats["total_packets"] += 1
                self.stats["protocols"][parsed["protocol"]] += 1
                
                if parsed["src_ip"]:
                    self.stats["top_src"][parsed["src_ip"]] += 1
                if parsed["dst_ip"]:
                    self.stats["top_dst"][parsed["dst_ip"]] += 1
                if parsed["dst_port"]:
                    self.stats["top_ports"][parsed["dst_port"]] += 1

                # Log packet
                log_packet_json(parsed)
                
                # Analyze packet
                self._analyze(parsed)
                
            except Empty:
                continue
            except Exception as e:
                self.stats["dropped_packets"] += 1
                # print(f"Error processing packet: {e}")

    def _analyze(self, parsed: dict):
        current_time = parsed["timestamp"]
        src_ip = parsed["src_ip"]
        if not src_ip: return

        # ICMP Flood Check
        if parsed["protocol"] == "ICMP":
            rule = self.rule_engine.get_rule("ICMP_FLOOD")
            if rule:
                self.windows["ICMP"][src_ip].append(current_time)
                self.windows["ICMP"][src_ip] = self._clean_window(self.windows["ICMP"][src_ip], current_time, rule["window"])
                if len(self.windows["ICMP"][src_ip]) > rule["threshold"]:
                    self._trigger_alert("ICMP_FLOOD", rule, src_ip, f"{len(self.windows['ICMP'][src_ip])} packets in {rule['window']}s")
                    self.windows["ICMP"][src_ip].clear() # Reset after alert

        # SYN Flood Check
        if parsed["protocol"] == "TCP" and parsed["flags"] == "S":
            rule = self.rule_engine.get_rule("SYN_FLOOD")
            if rule:
                self.windows["SYN"][src_ip].append(current_time)
                self.windows["SYN"][src_ip] = self._clean_window(self.windows["SYN"][src_ip], current_time, rule["window"])
                if len(self.windows["SYN"][src_ip]) > rule["threshold"]:
                    self._trigger_alert("SYN_FLOOD", rule, src_ip, f"{len(self.windows['SYN'][src_ip])} SYN packets in {rule['window']}s")
                    self.windows["SYN"][src_ip].clear()

        # UDP Flood Check
        if parsed["protocol"] == "UDP":
            rule = self.rule_engine.get_rule("UDP_FLOOD")
            if rule:
                self.windows["UDP"][src_ip].append(current_time)
                self.windows["UDP"][src_ip] = self._clean_window(self.windows["UDP"][src_ip], current_time, rule["window"])
                if len(self.windows["UDP"][src_ip]) > rule["threshold"]:
                    self._trigger_alert("UDP_FLOOD", rule, src_ip, f"{len(self.windows['UDP'][src_ip])} UDP packets in {rule['window']}s")
                    self.windows["UDP"][src_ip].clear()
                    
        # DNS Flood Check
        if parsed["protocol"] == "DNS":
            rule = self.rule_engine.get_rule("DNS_FLOOD")
            if rule:
                self.windows["DNS"][src_ip].append(current_time)
                self.windows["DNS"][src_ip] = self._clean_window(self.windows["DNS"][src_ip], current_time, rule["window"])
                if len(self.windows["DNS"][src_ip]) > rule["threshold"]:
                    self._trigger_alert("DNS_FLOOD", rule, src_ip, f"{len(self.windows['DNS'][src_ip])} DNS packets in {rule['window']}s")
                    self.windows["DNS"][src_ip].clear()

        # SSH Brute Force
        if parsed["protocol"] == "TCP" and parsed["dst_port"] == 22:
            # A heuristic: Counting frequent connections to port 22 from same IP. 
            # Real brute force detection requires inspecting payloads or host logs, but we approximate by connection rate.
            rule = self.rule_engine.get_rule("SSH_BRUTE_FORCE")
            if rule and parsed["flags"] == "S":
                self.windows["SSH"][src_ip].append(current_time)
                self.windows["SSH"][src_ip] = self._clean_window(self.windows["SSH"][src_ip], current_time, rule["window"])
                if len(self.windows["SSH"][src_ip]) > rule["threshold"]:
                    self._trigger_alert("SSH_BRUTE_FORCE", rule, src_ip, f"{len(self.windows['SSH'][src_ip])} SSH connection attempts in {rule['window']}s")
                    self.windows["SSH"][src_ip].clear()

        # Port Scan Check
        if parsed["protocol"] in ["TCP", "UDP"]:
            rule = self.rule_engine.get_rule("PORT_SCAN")
            if rule:
                self.windows["PORTS"][src_ip].add((parsed["dst_port"], current_time))
                self.windows["PORTS"][src_ip] = self._clean_port_window(self.windows["PORTS"][src_ip], current_time, rule["window"])
                
                # Count unique ports
                unique_ports = len({item[0] for item in self.windows["PORTS"][src_ip]})
                if unique_ports > rule["threshold"]:
                    self._trigger_alert("PORT_SCAN", rule, src_ip, f"Scanned {unique_ports} unique ports in {rule['window']}s")
                    self.windows["PORTS"][src_ip].clear()

    def _trigger_alert(self, rule_name: str, rule: dict, src_ip: str, extra: str):
        self.stats["alerts_generated"] += 1
        log_alert(rule["severity"], rule_name, src_ip, extra)
        self.recent_alerts.insert(0, (rule["severity"], rule_name, src_ip, time.strftime("%H:%M:%S")))
        if len(self.recent_alerts) > 10:
            self.recent_alerts.pop()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._process, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
