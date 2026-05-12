"""
TURNBOUND - Event Bus System
Event-driven architecture for decoupling game systems
"""

from typing import Callable, Dict, Any, List


class EventBus:
    """Central event bus for game-wide communication"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to an event"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Unsubscribe from an event"""
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass
    
    def trigger(self, event_name: str, data: Any = None) -> None:
        """Trigger an event with optional data"""
        if event_name in self._listeners:
            for callback in self._listeners[event_name][:]:  # Copy list to allow modification during iteration
                try:
                    callback(data)
                except Exception as e:
                    print(f"Event handler error for '{event_name}': {e}")
    
    def clear(self) -> None:
        """Clear all listeners"""
        self._listeners.clear()
    
    def has_listeners(self, event_name: str) -> bool:
        """Check if an event has any listeners"""
        return event_name in self._listeners and len(self._listeners[event_name]) > 0
