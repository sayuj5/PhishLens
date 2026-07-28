import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
RULES_DIR = os.path.join(BASE_DIR, 'rules')

ALERTS_LOG = os.path.join(LOG_DIR, 'alerts.log')
PACKETS_LOG = os.path.join(LOG_DIR, 'packets.log')
JSON_LOG_DIR = os.path.join(LOG_DIR, 'json')

def setup_directories():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(JSON_LOG_DIR, exist_ok=True)
    os.makedirs(RULES_DIR, exist_ok=True)
