from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseDiscoveryProvider(ABC):
    """
    Abstract base class for all discovery providers.
    """
    
    @abstractmethod
    async def is_reachable(self, ip: str, timeout_ms: int = 1000) -> bool:
        """
        Check if a host is reachable (e.g. ICMP ping or TCP ping).
        """
        pass
        
    @abstractmethod
    async def scan_ports(self, ip: str, ports: List[int], timeout_ms: int = 1000) -> List[int]:
        """
        Scan a list of ports and return the open ones.
        """
        pass
        
    @abstractmethod
    async def grab_banner(self, ip: str, port: int, timeout_ms: int = 2000) -> str:
        """
        Attempt to connect to a port and receive its banner.
        """
        pass
        
    @abstractmethod
    async def fingerprint_os(self, ip: str, open_ports: List[int]) -> Dict[str, Any]:
        """
        Attempt to guess the OS based on open ports or other heuristics.
        Returns a dict e.g. {"os": "Linux", "vendor": "Ubuntu"}
        """
        pass
