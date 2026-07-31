# Discovery module package
from backend.discovery.manager import manager
from backend.discovery.events import bus

__all__ = ["manager", "bus"]
