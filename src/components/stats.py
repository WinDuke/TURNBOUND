from dataclasses import dataclass

@dataclass
class Stats:
    """Компонент характеристик сущности."""
    power: int = 5
    defense: int = 0
    crit_chance: float = 0.1
    crit_mult: float = 1.5
    speed: int = 1
    evasion: float = 0.0
