from dataclasses import dataclass

@dataclass
class Energy:
    """Компонент энергии для использования навыков."""
    current: int
    max_energy: int
    
    def consume(self, amount: int) -> bool:
        """Потребить энергию. Возвращает True если успешно."""
        if self.current >= amount:
            self.current -= amount
            return True
        return False
        
    def restore(self, amount: int):
        """Восстановить энергию."""
        self.current = min(self.max_energy, self.current + amount)
