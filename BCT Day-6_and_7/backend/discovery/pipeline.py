import ipaddress
from typing import Dict, Any, List
from backend.discovery.providers.base import BaseDiscoveryProvider
from backend.logger import discovery_logger
from backend.database import SessionLocal
from backend.models import ScanScope, ScanProfile

class DiscoveryPipeline:
    def __init__(self, provider: BaseDiscoveryProvider):
        self.provider = provider
        
        # Define some common port profiles
        self.port_profiles = {
            "top_10": [21, 22, 23, 25, 80, 110, 139, 443, 445, 3389],
            "top_100": list(range(1, 101)) + [135, 139, 445, 1433, 3306, 3389, 5432, 8080, 8443],
            "all": list(range(1, 65536))
        }

    def _is_in_scope(self, ip: str) -> bool:
        """
        Check if the IP is within any active ScanScope.
        If no scopes exist, assume global authorization (for initial development).
        In strict mode, deny if no scopes.
        """
        db = SessionLocal()
        try:
            scopes = db.query(ScanScope).filter(ScanScope.is_active == True).all()
            if not scopes:
                return True # Fail-open for now if no scopes configured
                
            ip_obj = ipaddress.ip_address(ip)
            for scope in scopes:
                try:
                    network = ipaddress.ip_network(scope.target, strict=False)
                    if ip_obj in network:
                        return True
                except ValueError:
                    if ip == scope.target:
                        return True
            return False
        finally:
            db.close()

    def _get_ports_for_profile(self, profile: ScanProfile) -> List[int]:
        if not profile or not profile.ports:
            return self.port_profiles["top_10"]
            
        p = profile.ports.lower()
        if p in self.port_profiles:
            return self.port_profiles[p]
            
        # Parse custom comma separated list
        try:
            return [int(x.strip()) for x in p.split(",")]
        except ValueError:
            return self.port_profiles["top_10"]

    async def execute(self, ip: str, profile: ScanProfile = None) -> Dict[str, Any]:
        """
        Runs the 6-stage discovery pipeline.
        """
        # Set defaults from profile
        timeout_ms = profile.timeout_ms if profile else 2000
        ports = self._get_ports_for_profile(profile)
        
        # Stage 1: Scope Validation
        if not self._is_in_scope(ip):
            discovery_logger.warning(f"Target {ip} is out of authorized scope.")
            return {"ip": ip, "status": "out_of_scope"}

        # Stage 2: Reachability
        reachable = await self.provider.is_reachable(ip, timeout_ms)
        if not reachable:
            return {"ip": ip, "status": "offline"}
            
        # Stage 3: Port Scan
        open_ports = await self.provider.scan_ports(ip, ports, timeout_ms)
        
        # Stage 4: Banner Grab & Service Identification
        services = []
        for port in open_ports:
            banner = await self.provider.grab_banner(ip, port, timeout_ms)
            
            # Simple service name mapping
            svc_name = "unknown"
            if port == 22: svc_name = "ssh"
            elif port in (80, 8080): svc_name = "http"
            elif port in (443, 8443): svc_name = "https"
            elif port == 3389: svc_name = "rdp"
            elif port == 445: svc_name = "smb"
            elif port == 1433: svc_name = "mssql"
            elif port == 3306: svc_name = "mysql"
            elif port == 5432: svc_name = "postgresql"
            
            # Extract basic version from banner if present
            version = "Unknown"
            if "SSH" in banner:
                version = banner.split()[0]
            elif "Server: " in banner:
                for line in banner.split('\n'):
                    if line.startswith("Server: "):
                        version = line.replace("Server: ", "").strip()
                        break
            
            services.append({
                "port": port,
                "protocol": "tcp",
                "service": svc_name,
                "banner": banner[:100] if banner else None,
                "version": version
            })

        # Stage 5: OS Fingerprint
        os_info = await self.provider.fingerprint_os(ip, open_ports)
        
        # Stage 6: Format Results
        return {
            "ip": ip,
            "status": "online",
            "os": os_info.get("os", "Unknown"),
            "vendor": os_info.get("vendor", "Unknown"),
            "hostname": None, # DNS reverse lookup could be added here
            "mac": None,      # ARP lookup could be added here for local networks
            "services": services
        }
