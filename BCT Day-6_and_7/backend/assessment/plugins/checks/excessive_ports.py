"""
Plugin: Excessive Open Ports / Missing Firewall
Flags assets that expose an unusually large number of open ports, suggesting
insufficient firewall controls or misconfigured security groups.
"""
from typing import Any, Dict, List

from backend.assessment.plugins.base import BasePlugin, FindingData

DEFAULT_THRESHOLDS = {
    "low": 10,      # >10 ports = Low finding
    "medium": 25,   # >25 ports = Medium finding
    "high": 50,     # >50 ports = High finding
}


class ExcessivePortsPlugin(BasePlugin):
    PLUGIN_ID = "excessive_ports_check"
    NAME = "Excessive Open Ports / Insufficient Firewall"
    VERSION = "1.0.0"
    CATEGORY = "config"
    DESCRIPTION = (
        "Identifies assets exposing an unusually high number of open ports, "
        "which may indicate missing firewall controls."
    )

    async def run(self, asset: Dict[str, Any], config: Dict[str, Any]) -> List[FindingData]:
        findings: List[FindingData] = []
        ports = asset.get("ports", [])
        count = len(ports)

        thresholds = {
            "low": config.get("threshold_low", DEFAULT_THRESHOLDS["low"]),
            "medium": config.get("threshold_medium", DEFAULT_THRESHOLDS["medium"]),
            "high": config.get("threshold_high", DEFAULT_THRESHOLDS["high"]),
        }

        severity: str = ""
        if count > thresholds["high"]:
            severity = "high"
        elif count > thresholds["medium"]:
            severity = "medium"
        elif count > thresholds["low"]:
            severity = "low"

        if severity:
            port_list = ", ".join(str(p["port_number"]) for p in ports[:20])
            if count > 20:
                port_list += f" … (+{count - 20} more)"
            findings.append(FindingData(
                title=f"Excessive Open Ports Detected ({count} ports)",
                description=(
                    f"{asset.get('ip_address', 'This host')} has {count} open TCP ports, "
                    f"exceeding the recommended maximum of {thresholds['low']}. "
                    f"This may indicate insufficient network-level firewall controls or "
                    f"unnecessary services running on the host."
                ),
                severity=severity,
                category="config",
                evidence=f"Open ports detected: {port_list}",
                remediation=(
                    "Apply a host-based firewall policy (iptables/ufw/Windows Firewall) to restrict "
                    "access to only required service ports. Review and disable unnecessary services. "
                    "Apply a principle of least privilege to network access."
                ),
                references=[],
            ))
        return findings
