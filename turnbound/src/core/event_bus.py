"""Event bus for game-wide event handling."""

from typing import Callable, Any
from collections import defaultdict


class EventBus:
    """Central event dispatcher for the game."""

    def __init__(self):
        self._listeners: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event type."""
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event type."""
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit an event to all subscribers."""
        for callback in self._listeners.get(event_type, []):
            try:
                if data is not None:
                    callback(data)
                else:
                    callback()
            except Exception as e:
                # Log error but don't break event chain
                print(f"Event handler error for {event_type}: {e}")

    def clear(self) -> None:
        """Clear all listeners."""
        self._listeners.clear()


# Global event types
EVENT_HIT = "hit"
EVENT_CRIT = "crit"
EVENT_KILL = "kill"
EVENT_MOVE = "move"
EVENT_DASH = "dash"
EVENT_STATUS_APPLY = "status_apply"
EVENT_STATUS_REMOVE = "status_remove"
EVENT_LEVELUP = "levelup"
EVENT_WAVE_COMPLETE = "wave_complete"
EVENT_BOSS_PHASE_CHANGE = "boss_phase_change"
EVENT_SKILL_USE = "skill_use"
EVENT_DAMAGE_DEALT = "damage_dealt"
EVENT_HEAL = "heal"
EVENT_ENERGY_GAIN = "energy_gain"
EVENT_ENERGY_SPEND = "energy_spend"
