"""
Assessment __init__ – seeds the plugin registry into the DB on startup.
"""
from backend.assessment.engine import engine
from backend.assessment.plugins.registry import registry


def seed_plugins(db_session_factory) -> None:
    """Register all discovered plugins into the Plugin table if not already present."""
    from backend import models
    registry.discover()
    db = db_session_factory()
    try:
        for meta in registry.list_plugins():
            existing = db.query(models.Plugin).filter(
                models.Plugin.plugin_id == meta["plugin_id"]
            ).first()
            if not existing:
                db.add(models.Plugin(
                    plugin_id=meta["plugin_id"],
                    name=meta["name"],
                    version=meta["version"],
                    author=meta["author"],
                    category=meta["category"],
                    description=meta["description"],
                ))
        db.commit()
    finally:
        db.close()
