import logging
import json
import os
import time
from .config import ALERTS_LOG, PACKETS_LOG, JSON_LOG_DIR, setup_directories

# Ensure directories exist
setup_directories()

# Configure basic logging
alert_logger = logging.getLogger("Alerts")
alert_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(ALERTS_LOG)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)
alert_logger.addHandler(file_handler)

def log_alert(severity: str, rule_name: str, src_ip: str, message: str):
    log_msg = f"{rule_name} | Source: {src_ip} | {message}"
    if severity.upper() in ["HIGH", "CRITICAL"]:
        alert_logger.error(log_msg)
    elif severity.upper() == "MEDIUM":
        alert_logger.warning(log_msg)
    else:
        alert_logger.info(log_msg)

def log_packet_json(packet_info: dict):
    timestamp = time.strftime("%Y%m%d_%H")
    json_file = os.path.join(JSON_LOG_DIR, f"packets_{timestamp}.json")
    with open(json_file, 'a') as f:
        json.dump(packet_info, f)
        f.write('\n')
