import asyncio
from typing import Callable, List, Dict, Any
from backend.logger import discovery_logger

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        discovery_logger.debug(f"Subscribed to {event_type}. Total: {len(self.subscribers[event_type])}")

    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            discovery_logger.debug(f"Unsubscribed from {event_type}.")

    async def publish(self, event_type: str, data: Any):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    await callback(data)
                except Exception as e:
                    discovery_logger.error(f"Error in event subscriber for {event_type}: {e}")

bus = EventBus()
