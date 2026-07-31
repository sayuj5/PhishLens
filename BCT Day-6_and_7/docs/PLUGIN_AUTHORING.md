# Plugin Authoring Guide

BlackFalcon's Assessment Engine is built on a modular plugin architecture. You can easily add new vulnerability checks by creating a new Python file in the `backend/assessment/plugins/checks/` directory.

## Creating a Plugin

1. Create a file (e.g., `my_check.py`).
2. Import `BasePlugin` and `FindingData`.
3. Subclass `BasePlugin` and define the required metadata.
4. Implement the `async def run(self, asset, config)` method.

### Example

```python
from typing import Any, Dict, List
from backend.assessment.plugins.base import BasePlugin, FindingData

class MyCustomPlugin(BasePlugin):
    PLUGIN_ID = "my_custom_check"
    NAME = "My Custom Vulnerability Check"
    VERSION = "1.0.0"
    CATEGORY = "config"
    DESCRIPTION = "Checks for a specific misconfiguration."

    async def run(self, asset: Dict[str, Any], config: Dict[str, Any]) -> List[FindingData]:
        findings = []
        
        # Example logic
        if asset.get("os") == "Windows XP":
            findings.append(FindingData(
                title="Unsupported OS Detected",
                description="Windows XP is end-of-life and highly vulnerable.",
                severity="critical",
                category="config",
                evidence="OS fingerprint returned Windows XP",
                remediation="Upgrade to a supported OS immediately."
            ))
            
        return findings
```

## Plugin Registration
You do **not** need to manually register the plugin. The engine automatically scans the `checks/` directory on startup and seeds any new plugins into the database.
