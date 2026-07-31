"""
Plugin: High-Risk Open Ports
Flags assets exposing services on ports that present elevated risk in most environments.
"""
from typing import Any, Dict, List

from backend.assessment.plugins.base import BasePlugin, FindingData

# Ports that are commonly abused or indicate weak security posture
RISKY_PORTS: Dict[int, Dict[str, str]] = {
    21:   {"service": "FTP", "severity": "high",
           "reason": "FTP transmits credentials in plaintext and is frequently exploited.",
           "remediation": "Disable FTP. Use SFTP or SCP for secure file transfers."},
    23:   {"service": "Telnet", "severity": "critical",
           "reason": "Telnet transmits all data, including credentials, in plaintext.",
           "remediation": "Disable Telnet immediately. Replace with SSH."},
    135:  {"service": "MS-RPC", "severity": "medium",
           "reason": "MS-RPC is a common vector for lateral movement and exploitation.",
           "remediation": "Restrict port 135 with a host firewall. Disable unnecessary RPC services."},
    139:  {"service": "NetBIOS", "severity": "medium",
           "reason": "NetBIOS exposes machine names and can be leveraged for enumeration.",
           "remediation": "Disable NetBIOS over TCP/IP where not required."},
    445:  {"service": "SMB", "severity": "high",
           "reason": "SMB is a prime target (EternalBlue, WannaCry). Exposure on non-Windows systems is unusual.",
           "remediation": "Restrict SMB to required internal hosts. Keep systems patched. Disable SMBv1."},
    1433: {"service": "MSSQL", "severity": "high",
           "reason": "Directly exposed database servers are a high-value target.",
           "remediation": "Place database behind a firewall. Use a VPN or bastion host for remote access."},
    3306: {"service": "MySQL", "severity": "high",
           "reason": "Directly exposed database servers are a high-value target.",
           "remediation": "Restrict MySQL to localhost or internal networks. Do not expose publicly."},
    3389: {"service": "RDP", "severity": "high",
           "reason": "RDP is frequently targeted by brute-force and credential stuffing attacks.",
           "remediation": "Restrict RDP access with Network Level Authentication and IP allowlisting. Use a VPN."},
    5432: {"service": "PostgreSQL", "severity": "high",
           "reason": "Directly exposed database servers are a high-value target.",
           "remediation": "Restrict PostgreSQL to localhost or internal networks."},
    5900: {"service": "VNC", "severity": "critical",
           "reason": "VNC is frequently exposed without authentication or uses weak passwords.",
           "remediation": "Disable VNC if not required. Require strong authentication and tunnel via SSH or VPN."},
    6379: {"service": "Redis", "severity": "critical",
           "reason": "Redis is commonly misconfigured with no authentication, allowing arbitrary data access.",
           "remediation": "Bind Redis to localhost. Enable requirepass. Never expose Redis publicly."},
    27017: {"service": "MongoDB", "severity": "critical",
            "reason": "MongoDB is frequently exposed with no authentication enabled.",
            "remediation": "Enable MongoDB authentication. Bind to internal addresses only."},
}


class OpenPortsPlugin(BasePlugin):
    PLUGIN_ID = "open_ports_check"
    NAME = "High-Risk Open Ports"
    VERSION = "1.1.0"
    CATEGORY = "port"
    DESCRIPTION = "Identifies open ports associated with high-risk or inherently insecure services."

    async def run(self, asset: Dict[str, Any], config: Dict[str, Any]) -> List[FindingData]:
        findings: List[FindingData] = []
        open_ports = {p["port_number"] for p in asset.get("ports", [])}

        for port, info in RISKY_PORTS.items():
            if port in open_ports:
                findings.append(FindingData(
                    title=f"High-Risk Port Open: {port}/{info['service']}",
                    description=(
                        f"Port {port} ({info['service']}) is open on {asset.get('ip_address', 'this host')}. "
                        f"{info['reason']}"
                    ),
                    severity=info["severity"],
                    category="port",
                    evidence=f"TCP/{port} responded during the last discovery scan.",
                    remediation=info["remediation"],
                    references=[],
                ))
        return findings
