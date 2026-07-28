import yaml
import os
from core.config import RULES_DIR

class RuleEngine:
    def __init__(self, rule_file="signatures.yaml"):
        self.rule_file = os.path.join(RULES_DIR, rule_file)
        self.rules = {}
        self.load_rules()

    def load_rules(self):
        if not os.path.exists(self.rule_file):
            self._create_default_rules()
            
        with open(self.rule_file, 'r') as f:
            try:
                self.rules = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Error parsing rules: {e}")
                self.rules = {}

    def get_rule(self, rule_name: str) -> dict:
        return self.rules.get(rule_name, {})

    def _create_default_rules(self):
        default_rules = {
            "ICMP_FLOOD": {
                "threshold": 100,
                "window": 2,
                "severity": "HIGH",
                "message": "Possible ICMP Flood"
            },
            "SYN_FLOOD": {
                "threshold": 200,
                "window": 2,
                "severity": "HIGH",
                "message": "Possible TCP SYN Flood"
            },
            "UDP_FLOOD": {
                "threshold": 500,
                "window": 1,
                "severity": "HIGH",
                "message": "Possible UDP Flood"
            },
            "SSH_BRUTE_FORCE": {
                "threshold": 5,
                "window": 60,
                "severity": "HIGH",
                "message": "SSH Brute Force Attempt"
            },
            "PORT_SCAN": {
                "threshold": 50,
                "window": 10,
                "severity": "MEDIUM",
                "message": "Port Scan Detected"
            },
            "DNS_FLOOD": {
                "threshold": 200,
                "window": 2,
                "severity": "MEDIUM",
                "message": "DNS Query Burst Detected"
            }
        }
        with open(self.rule_file, 'w') as f:
            yaml.dump(default_rules, f, default_flow_style=False)
