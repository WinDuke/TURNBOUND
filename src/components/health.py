from dataclasses import dataclass

@dataclass
class Health:
    """Компонент здоровья сущности."""
    current_hp: int
    max_hp: int
    
    def take_damage(self, amount: int) -> int:
        """Получить урон. Возвращает фактический полученный урон."""
        actual_dmg = max(0, amount)
        self.current_hp -= actual_dmg
        return actual_dmg
        
    def heal(self, amount: int):
        """Лечить сущность."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        
    def is_dead(self) -> bool:
        """Проверить, мертва ли сущность."""
        return self.current_hp <= 0
