from dataclasses import dataclass

@dataclass
class Faction:
    """Компонент фракции сущности (player, enemy, neutral)."""
    value: str = "neutral"
    
    def is_player(self) -> bool:
        return self.value == "player"
    
    def is_enemy(self) -> bool:
        return self.value == "enemy"
    
    def is_neutral(self) -> bool:
        return self.value == "neutral"
    
    def is_hostile_to(self, other: 'Faction') -> bool:
        """Проверить враждебность к другой фракции."""
        if self.value == "neutral" or other.value == "neutral":
            return False
        return self.value != other.value
