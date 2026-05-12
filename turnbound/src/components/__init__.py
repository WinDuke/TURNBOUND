"""Core ECS components."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Position:
    """Grid position component."""
    x: int = 0
    y: int = 0


@dataclass
class Renderable:
    """Rendering component for ASCII display."""
    symbol: str = "@"
    color: str = "#ffffff"
    bg_color: str | None = None
    bold: bool = False
    blink: bool = False
    render_priority: int = 0  # Higher = rendered on top


@dataclass
class Health:
    """Health points component."""
    current: int = 100
    max: int = 100

    @property
    def percent(self) -> float:
        return self.current / self.max if self.max > 0 else 0.0

    def damage(self, amount: int) -> int:
        """Apply damage and return actual damage dealt."""
        actual = min(amount, self.current)
        self.current = max(0, self.current - amount)
        return actual

    def heal(self, amount: int) -> int:
        """Heal and return actual healing done."""
        old = self.current
        self.current = min(self.max, self.current + amount)
        return self.current - old

    def is_alive(self) -> bool:
        return self.current > 0


@dataclass
class Energy:
    """Energy/resource component for skills."""
    current: int = 100
    max: int = 100
    regen: int = 5  # Per turn

    def spend(self, amount: int) -> bool:
        """Try to spend energy. Returns True if successful."""
        if self.current >= amount:
            self.current -= amount
            return True
        return False

    def restore(self, amount: int) -> int:
        """Restore energy and return actual amount restored."""
        old = self.current
        self.current = min(self.max, self.current + amount)
        return self.current - old


@dataclass
class Stats:
    """Combat statistics component."""
    power: int = 10  # Damage scaling
    defense: int = 0  # Flat mitigation
    crit_chance: float = 0.05  # 5% base
    crit_multiplier: float = 2.0
    speed: int = 0  # Turn order modifier
    evasion: float = 0.0  # Dodge chance


@dataclass
class Skills:
    """Known abilities component."""
    active: list[dict] = field(default_factory=list)  # List of skill dicts
    passive: list[dict] = field(default_factory=list)  # Passive abilities
    triggered: list[dict] = field(default_factory=list)  # Event-triggered


@dataclass
class Cooldowns:
    """Cooldown tracking component."""
    cooldowns: dict[str, int] = field(default_factory=dict)  # skill_id -> turns remaining

    def add(self, skill_id: str, turns: int) -> None:
        self.cooldowns[skill_id] = turns

    def tick(self) -> None:
        """Decrease all cooldowns by 1."""
        for skill_id in list(self.cooldowns.keys()):
            self.cooldowns[skill_id] -= 1
            if self.cooldowns[skill_id] <= 0:
                del self.cooldowns[skill_id]

    def is_ready(self, skill_id: str) -> bool:
        return skill_id not in self.cooldowns

    def get_remaining(self, skill_id: str) -> int:
        return self.cooldowns.get(skill_id, 0)


@dataclass
class AI:
    """AI behavior component."""
    behavior_type: str = "aggressive"  # aggressive, defensive, tactical, etc.
    target_id: int | None = None
    utility_weights: dict[str, float] = field(default_factory=dict)
    elite_modifier: str | None = None  # Aggressive, Tactical, Frenzied, Coward


@dataclass
class Statuses:
    """Active status effects component."""
    effects: dict[str, dict] = field(default_factory=dict)  # status_id -> {duration, stacks, data}

    def add(self, status_id: str, duration: int, stacks: int = 1, data: dict | None = None) -> None:
        if status_id in self.effects:
            existing = self.effects[status_id]
            existing["duration"] = max(existing["duration"], duration)
            existing["stacks"] = min(existing.get("max_stacks", 999), existing["stacks"] + stacks)
        else:
            self.effects[status_id] = {
                "duration": duration,
                "stacks": stacks,
                "data": data or {}
            }

    def remove(self, status_id: str) -> None:
        self.effects.pop(status_id, None)

    def has(self, status_id: str) -> bool:
        return status_id in self.effects

    def get(self, status_id: str) -> dict | None:
        return self.effects.get(status_id)

    def tick(self) -> list[str]:
        """Tick down durations and return expired status IDs."""
        expired = []
        for status_id in list(self.effects.keys()):
            self.effects[status_id]["duration"] -= 1
            if self.effects[status_id]["duration"] <= 0:
                expired.append(status_id)
                del self.effects[status_id]
        return expired


@dataclass
class Faction:
    """Faction alignment component."""
    alignment: str = "neutral"  # player, enemy, neutral, boss


@dataclass
class Tags:
    """Gameplay tags for synergies."""
    tags: set[str] = field(default_factory=set)

    def add(self, tag: str) -> None:
        self.tags.add(tag)

    def remove(self, tag: str) -> None:
        self.tags.discard(tag)

    def has(self, tag: str) -> bool:
        return tag in self.tags

    def has_any(self, tags: list[str]) -> bool:
        return any(tag in self.tags for tag in tags)

    def has_all(self, tags: list[str]) -> bool:
        return all(tag in self.tags for tag in tags)


@dataclass
class Level:
    """Experience and level component."""
    exp: int = 0
    level: int = 1
    exp_to_next: int = 100

    def add_exp(self, amount: int) -> bool:
        """Add EXP and return True if leveled up."""
        self.exp += amount
        if self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next = int(self.exp_to_next * 1.5)
            return True
        return False


@dataclass
class Inventory:
    """Item/component storage."""
    items: list[dict] = field(default_factory=list)
    max_size: int = 10


@dataclass
class Boss:
    """Boss-specific component."""
    phase: int = 1
    phases: list[dict] = field(default_factory=list)
    script_state: str = ""
    arena_effect: str | None = None
