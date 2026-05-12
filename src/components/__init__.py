"""
TURNBOUND - Components
Data-only components for ECS
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Position:
    """Grid coordinates"""
    x: int
    y: int


@dataclass
class Renderable:
    """ASCII symbol, color, render priority"""
    symbol: str
    color: str
    bg_color: str = "default"
    layer: int = 2  # 0=terrain, 1=objects, 2=units, 3=effects
    glow: bool = False
    animated: bool = False


@dataclass
class Health:
    """Current HP and max HP"""
    current_hp: int
    max_hp: int
    
    def take_damage(self, amount: int) -> int:
        """Apply damage and return actual damage dealt"""
        actual_dmg = max(0, amount)
        self.current_hp -= actual_dmg
        return actual_dmg
    
    def heal(self, amount: int) -> int:
        """Heal and return actual healing done"""
        actual_heal = max(0, amount)
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + actual_heal)
        return self.current_hp - old_hp
    
    def is_dead(self) -> bool:
        """Check if entity is dead"""
        return self.current_hp <= 0
    
    def hp_percent(self) -> float:
        """Get HP as percentage"""
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0.0


@dataclass
class Energy:
    """Skill resource"""
    current: int
    max_energy: int
    
    def consume(self, amount: int) -> bool:
        """Consume energy, return True if successful"""
        if self.current >= amount:
            self.current -= amount
            return True
        return False
    
    def restore(self, amount: int) -> int:
        """Restore energy, return actual amount restored"""
        old = self.current
        self.current = min(self.max_energy, self.current + amount)
        return self.current - old
    
    def is_empty(self) -> bool:
        """Check if energy is empty"""
        return self.current <= 0


@dataclass
class Stats:
    """Combat statistics"""
    power: int = 5
    defense: int = 0
    crit_chance: float = 0.1
    crit_mult: float = 1.5
    speed: int = 1
    evasion: float = 0.0
    # Resistances (0-1 scale)
    resist_physical: float = 0.0
    resist_fire: float = 0.0
    resist_frost: float = 0.0
    resist_lightning: float = 0.0
    resist_void: float = 0.0
    resist_poison: float = 0.0
    resist_blood: float = 0.0


@dataclass
class Skills:
    """Known abilities and cooldowns"""
    known: List[str] = field(default_factory=list)
    cooldowns: Dict[str, int] = field(default_factory=dict)
    
    def add_skill(self, skill_id: str) -> None:
        """Add a skill to known skills"""
        if skill_id not in self.known:
            self.known.append(skill_id)
            self.cooldowns[skill_id] = 0
    
    def remove_skill(self, skill_id: str) -> None:
        """Remove a skill"""
        if skill_id in self.known:
            self.known.remove(skill_id)
        if skill_id in self.cooldowns:
            del self.cooldowns[skill_id]
    
    def tick_cooldowns(self) -> None:
        """Decrease all cooldowns by 1"""
        for k in list(self.cooldowns.keys()):
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1
    
    def can_use(self, skill_id: str) -> bool:
        """Check if a skill can be used"""
        return skill_id in self.known and self.cooldowns.get(skill_id, 0) == 0
    
    def get_cooldown(self, skill_id: str) -> int:
        """Get current cooldown for a skill"""
        return self.cooldowns.get(skill_id, 0)
    
    def set_cooldown(self, skill_id: str, turns: int) -> None:
        """Set cooldown for a skill"""
        if skill_id in self.known:
            self.cooldowns[skill_id] = turns


@dataclass
class Cooldowns:
    """Generic cooldown tracker (for non-skill abilities)"""
    timers: Dict[str, int] = field(default_factory=dict)
    
    def add(self, name: str, turns: int) -> None:
        """Add or reset a cooldown"""
        self.timers[name] = turns
    
    def tick(self) -> List[str]:
        """Tick all cooldowns, return expired ones"""
        expired = []
        for name in list(self.timers.keys()):
            self.timers[name] -= 1
            if self.timers[name] <= 0:
                expired.append(name)
                del self.timers[name]
        return expired
    
    def is_ready(self, name: str) -> bool:
        """Check if a cooldown is ready"""
        return name not in self.timers or self.timers[name] <= 0


@dataclass
class AI:
    """AI behavior profile"""
    behavior_type: str = "aggressive"  # aggressive, tactical, coward, frenzied
    params: Dict[str, Any] = field(default_factory=dict)
    target_override: Optional[int] = None  # Force target this entity ID


@dataclass
class Statuses:
    """Active status effects"""
    active: List['StatusEffect'] = field(default_factory=list)
    
    def add_effect(self, effect: 'StatusEffect') -> None:
        """Add a status effect"""
        # Check for existing effect to stack
        existing = next((s for s in self.active if s.id == effect.id), None)
        if existing:
            existing.duration = max(existing.duration, effect.duration)
            existing.stacks += effect.stacks
        else:
            self.active.append(effect)
    
    def remove_effect(self, effect_id: str) -> bool:
        """Remove a status effect by ID"""
        for i, eff in enumerate(self.active):
            if eff.id == effect_id:
                self.active.pop(i)
                return True
        return False
    
    def has_effect(self, effect_id: str) -> bool:
        """Check if entity has a specific effect"""
        return any(e.id == effect_id for e in self.active)
    
    def get_effect(self, effect_id: str) -> Optional['StatusEffect']:
        """Get a specific effect"""
        return next((e for e in self.active if e.id == effect_id), None)
    
    def tick(self) -> List['StatusEffect']:
        """Tick all effects, return expired ones"""
        expired = []
        for eff in self.active[:]:
            eff.duration -= 1
            if eff.duration <= 0:
                expired.append(eff)
                self.active.remove(eff)
        return expired
    
    def clear(self) -> None:
        """Remove all effects"""
        self.active.clear()


@dataclass
class StatusEffect:
    """A single status effect instance"""
    id: str
    duration: int
    stacks: int = 1
    source_id: Optional[int] = None  # Entity that applied this


@dataclass
class Faction:
    """Faction alignment"""
    value: str = "neutral"  # player, enemy, neutral
    
    def is_hostile_to(self, other: 'Faction') -> bool:
        """Check if hostile to another faction"""
        if self.value == "player":
            return other.value == "enemy"
        elif self.value == "enemy":
            return other.value == "player"
        return False  # Neutral is not hostile to anyone


@dataclass
class Tags:
    """Gameplay tags for synergies and triggers"""
    values: List[str] = field(default_factory=list)
    
    def add(self, tag: str) -> None:
        """Add a tag if not present"""
        if tag not in self.values:
            self.values.append(tag)
    
    def remove(self, tag: str) -> bool:
        """Remove a tag"""
        if tag in self.values:
            self.values.remove(tag)
            return True
        return False
    
    def has(self, tag: str) -> bool:
        """Check if entity has a tag"""
        return tag in self.values
    
    def has_any(self, tags: List[str]) -> bool:
        """Check if entity has any of the given tags"""
        return any(t in self.values for t in tags)
    
    def has_all(self, tags: List[str]) -> bool:
        """Check if entity has all of the given tags"""
        return all(t in self.values for t in tags)


@dataclass
class Experience:
    """Experience and level tracking"""
    current_exp: int = 0
    level: int = 1
    exp_to_next: int = 100
    
    def add_exp(self, amount: int) -> bool:
        """Add experience, return True if leveled up"""
        self.current_exp += amount
        if self.current_exp >= self.exp_to_next:
            self.level_up()
            return True
        return False
    
    def level_up(self) -> None:
        """Level up and adjust exp requirements"""
        self.current_exp -= self.exp_to_next
        self.level += 1
        self.exp_to_next = int(self.exp_to_next * 1.5)
    
    def get_exp_percent(self) -> float:
        """Get EXP progress as percentage"""
        return self.current_exp / self.exp_to_next if self.exp_to_next > 0 else 0.0
