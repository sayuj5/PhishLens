from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SEVERITY_WEIGHTS = {
    "critical": 10.0,
    "high": 7.0,
    "medium": 4.0,
    "low": 2.0,
    "info": 0.5,
}


@dataclass
class FindingData:
    """Structured result returned by a plugin."""
    title: str
    description: str
    severity: str  # critical | high | medium | low | info
    category: str
    evidence: str = ""
    remediation: str = ""
    references: List[str] = field(default_factory=list)

    @property
    def risk_score(self) -> float:
        return SEVERITY_WEIGHTS.get(self.severity, 0.5)


class BasePlugin(ABC):
    """
    Abstract base class for all BlackFalcon assessment plugins.

    Every plugin must declare its metadata as class-level attributes
    and implement the `run` coroutine.
    """

    PLUGIN_ID: str = ""
    NAME: str = ""
    VERSION: str = "1.0.0"
    AUTHOR: str = "BlackFalcon"
    CATEGORY: str = ""          # port | service | banner | config | network
    DESCRIPTION: str = ""
    SUPPORTED_OS: List[str] = []     # empty = all OS
    SUPPORTED_ASSET_TYPES: List[str] = []  # empty = all types

    @classmethod
    def metadata(cls) -> Dict[str, Any]:
        return {
            "plugin_id": cls.PLUGIN_ID,
            "name": cls.NAME,
            "version": cls.VERSION,
            "author": cls.AUTHOR,
            "category": cls.CATEGORY,
            "description": cls.DESCRIPTION,
            "supported_os": cls.SUPPORTED_OS,
        }

    @abstractmethod
    async def run(self, asset: Dict[str, Any], config: Dict[str, Any]) -> List[FindingData]:
        """
        Execute the plugin against a single asset dict.

        asset keys: id, ip_address, hostname, os, vendor, ports (list of dicts)
        Returns a list of FindingData instances (may be empty).
        """
        pass
