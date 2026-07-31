"""
Plugin: Unencrypted / Default Services
Detects services that transmit data in plaintext or use known default configurations.
"""
from typing import Any, Dict, List

from backend.assessment.plugins.base import BasePlugin, FindingData

# port -> (service_hint, severity, reason, remediation)
UNENCRYPTED: Dict[int, tuple] = {
    80:   ("HTTP", "medium",
           "HTTP traffic is unencrypted and susceptible to interception.",
           "Redirect all HTTP traffic to HTTPS (port 443). Enable HSTS."),
    21:   ("FTP", "high",
           "FTP transmits credentials and data in plaintext.",
           "Replace with SFTP or FTPS."),
    23:   ("Telnet", "critical",
           "Telnet is completely unencrypted.",
           "Replace with SSH immediately."),
    110:  ("POP3", "medium",
           "POP3 transmits email credentials in plaintext.",
           "Use POP3S (port 995) or migrate to IMAPS."),
    143:  ("IMAP", "medium",
           "IMAP transmits email credentials in plaintext.",
           "Use IMAPS (port 993)."),
    25:   ("SMTP", "low",
           "SMTP without STARTTLS may relay email in plaintext.",
           "Enforce STARTTLS on SMTP. Consider using port 587 with authentication."),
    161:  ("SNMP", "high",
           "SNMP v1/v2c uses community strings as plaintext passwords.",
           "Upgrade to SNMPv3 with auth and encryption. Restrict SNMP to management networks."),
    512:  ("rexec", "critical",
           "rexec is a legacy remote execution protocol with no encryption.",
           "Disable rexec. Use SSH."),
    513:  ("rlogin", "critical",
           "rlogin is a legacy remote login protocol with no encryption.",
           "Disable rlogin. Use SSH."),
    514:  ("rsh", "critical",
           "rsh allows unauthenticated remote shell commands.",
           "Disable rsh. Use SSH."),
}


class DefaultServicesPlugin(BasePlugin):
    PLUGIN_ID = "default_services_check"
    NAME = "Unencrypted / Insecure Services"
    VERSION = "1.0.0"
    CATEGORY = "service"
    DESCRIPTION = "Detects services transmitting data over unencrypted channels or known insecure defaults."

    async def run(self, asset: Dict[str, Any], config: Dict[str, Any]) -> List[FindingData]:
        findings: List[FindingData] = []
        open_ports = {p["port_number"] for p in asset.get("ports", [])}

        for port, (svc, severity, reason, remediation) in UNENCRYPTED.items():
            if port in open_ports:
                findings.append(FindingData(
                    title=f"Unencrypted Service Detected: {svc} (Port {port})",
                    description=(
                        f"{svc} is running on port {port} on {asset.get('ip_address', 'this host')}. "
                        f"{reason}"
                    ),
                    severity=severity,
                    category="service",
                    evidence=f"Port {port} ({svc}) responded during the last discovery scan.",
                    remediation=remediation,
                    references=[],
                ))
        return findings
