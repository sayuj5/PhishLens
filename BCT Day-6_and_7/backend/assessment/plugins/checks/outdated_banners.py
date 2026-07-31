"""
Plugin: Outdated Service Banners
Analyses service banners to identify potentially outdated or end-of-life software versions.
"""
import re
from typing import Any, Dict, List, Optional, Tuple

from backend.assessment.plugins.base import BasePlugin, FindingData

# (regex, service_name, min_safe_version_hint, severity, remediation)
BANNER_PATTERNS: List[Tuple] = [
    (r"OpenSSH[_\s](\d+\.\d+)", "OpenSSH", "8.0", "medium",
     "Upgrade OpenSSH to 8.0 or later. Older versions may have known vulnerabilities."),
    (r"Apache[/\s](\d+\.\d+\.\d+)", "Apache HTTP", "2.4.50", "medium",
     "Upgrade Apache to the latest 2.4.x release. Pre-2.4.50 has multiple CVEs."),
    (r"nginx[/\s](\d+\.\d+\.\d+)", "nginx", "1.22", "low",
     "Upgrade nginx to the latest stable release (1.22+)."),
    (r"vsftpd\s+(\d+\.\d+\.?\d*)", "vsftpd", "3.0", "medium",
     "Upgrade vsftpd to 3.0.x or later."),
    (r"ProFTPD[/\s](\d+\.\d+\.\d+)", "ProFTPD", "1.3.7", "medium",
     "Upgrade ProFTPD to 1.3.7 or later."),
    (r"Microsoft-IIS[/\s](\d+\.\d+)", "IIS", "10.0", "medium",
     "Upgrade IIS and ensure the underlying Windows Server is fully patched."),
    (r"OpenSSL[/\s](\d+\.\d+\.\d+)", "OpenSSL", "3.0", "high",
     "Upgrade OpenSSL to 3.x. Older versions have critical CVEs (e.g., Heartbleed, OpenSSL 1.x EOL issues)."),
    (r"Exim[/\s](\d+\.\d+)", "Exim MTA", "4.96", "medium",
     "Upgrade Exim to 4.96 or later."),
    (r"Postfix[/\s](\d+\.\d+\.\d+)", "Postfix", "3.7", "low",
     "Upgrade Postfix to the latest release."),
    (r"MySQL[/\s](\d+\.\d+\.\d+)", "MySQL", "8.0", "medium",
     "Upgrade MySQL to 8.0+ or use the latest 5.7.x patch. MySQL 5.6 is EOL."),
]


def _version_lt(v: str, minimum: str) -> bool:
    """Return True if v is less than minimum (basic semver comparison)."""
    try:
        def parts(s: str) -> List[int]:
            return [int(x) for x in re.split(r"[.\-]", s)[:3]]
        return parts(v) < parts(minimum)
    except Exception:
        return False


class OutdatedBannersPlugin(BasePlugin):
    PLUGIN_ID = "outdated_banners_check"
    NAME = "Outdated Service Banner Detection"
    VERSION = "1.2.0"
    CATEGORY = "banner"
    DESCRIPTION = "Analyses service banners to detect potentially outdated or end-of-life software."

    async def run(self, asset: Dict[str, Any], config: Dict[str, Any]) -> List[FindingData]:
        findings: List[FindingData] = []
        ports = asset.get("ports", [])

        banners_found: List[str] = []
        for p in ports:
            svc = p.get("service") or {}
            banner = svc.get("banner") or "" if isinstance(svc, dict) else ""
            if banner:
                banners_found.append(banner)

        all_banners = " ".join(banners_found)

        for pattern, svc_name, min_ver, severity, remediation in BANNER_PATTERNS:
            match = re.search(pattern, all_banners, re.IGNORECASE)
            if match:
                detected_version = match.group(1)
                if _version_lt(detected_version, min_ver):
                    findings.append(FindingData(
                        title=f"Potentially Outdated Software: {svc_name} {detected_version}",
                        description=(
                            f"{svc_name} version {detected_version} was detected on "
                            f"{asset.get('ip_address', 'this host')}. "
                            f"The minimum recommended version is {min_ver}. "
                            f"Older versions may contain known, publicly disclosed vulnerabilities."
                        ),
                        severity=severity,
                        category="banner",
                        evidence=f"Banner reported: '{match.group(0)}'",
                        remediation=remediation,
                        references=[],
                    ))
        return findings
