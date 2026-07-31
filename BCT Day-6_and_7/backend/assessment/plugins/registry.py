"""
Plugin Registry – auto-discovers and manages all assessment plugins.
"""
import importlib
import pkgutil
import inspect
import logging
from typing import Dict, List, Optional, Type

from backend.assessment.plugins.base import BasePlugin

logger = logging.getLogger("blackfalcon.assessment")


class PluginRegistry:
    _plugins: Dict[str, Type[BasePlugin]] = {}

    @classmethod
    def register(cls, plugin_cls: Type[BasePlugin]) -> None:
        if not plugin_cls.PLUGIN_ID:
            return
        cls._plugins[plugin_cls.PLUGIN_ID] = plugin_cls
        logger.debug(f"Registered plugin: {plugin_cls.PLUGIN_ID}")

    @classmethod
    def discover(cls) -> None:
        """Auto-import every module inside the checks/ package."""
        import backend.assessment.plugins.checks as checks_pkg
        for _, module_name, _ in pkgutil.iter_modules(checks_pkg.__path__):
            full = f"backend.assessment.plugins.checks.{module_name}"
            module = importlib.import_module(full)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BasePlugin) and obj is not BasePlugin:
                    cls.register(obj)
        logger.info(f"Plugin discovery complete. {len(cls._plugins)} plugins registered.")

    @classmethod
    def list_plugins(cls) -> List[Dict]:
        return [p.metadata() for p in cls._plugins.values()]

    @classmethod
    def get_plugin(cls, plugin_id: str) -> Optional[Type[BasePlugin]]:
        return cls._plugins.get(plugin_id)

    @classmethod
    def get_enabled_plugins(cls, enabled_ids: Optional[List[str]] = None) -> List[Type[BasePlugin]]:
        """
        Returns all registered plugins. If enabled_ids provided, filters to that subset.
        """
        if enabled_ids:
            return [cls._plugins[pid] for pid in enabled_ids if pid in cls._plugins]
        return list(cls._plugins.values())


registry = PluginRegistry()
