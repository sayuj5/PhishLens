import asyncio
import random
from backend.logger import discovery_logger

async def mock_scan_target(target: str, job_type: str) -> dict:
    """
    Simulates a network scan against a target.
    In a real implementation, this would use Nmap, Masscan, or asyncio sockets.
    """
    discovery_logger.info(f"Starting {job_type} scan on {target}...")
    
    # Simulate network delay
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # Randomly fail some hosts to simulate offline assets
    if random.random() < 0.2:
        return {"status": "offline"}
        
    # Generate mock data
    is_windows = random.choice([True, False])
    
    ports = [
        {"port": 80, "protocol": "tcp", "service": "http"},
        {"port": 443, "protocol": "tcp", "service": "https"},
    ]
    
    if is_windows:
        ports.append({"port": 3389, "protocol": "tcp", "service": "rdp"})
        ports.append({"port": 445, "protocol": "tcp", "service": "smb"})
        os_name = "Windows Server 2022"
        vendor = "Microsoft"
    else:
        ports.append({"port": 22, "protocol": "tcp", "service": "ssh"})
        os_name = "Ubuntu Linux 22.04"
        vendor = "Canonical"
        
    return {
        "status": "online",
        "ip_address": target,
        "hostname": f"host-{target.replace('.', '-')}",
        "mac_address": f"00:1A:2B:3C:{random.randint(10, 99)}:{random.randint(10, 99)}",
        "os": os_name,
        "vendor": vendor,
        "ports": ports
    }
