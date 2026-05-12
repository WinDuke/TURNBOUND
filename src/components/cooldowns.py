from dataclasses import dataclass

@dataclass
class Cooldowns:
    """Компонент общих кулдаунов (альтернатива Skills для глобальных КД)."""
    timers: dict = None
    
    def __post_init__(self):
        if self.timers is None:
            self.timers = {}
    
    def tick(self):
        """Уменьшить все таймеры на 1."""
        for k in list(self.timers.keys()):
            if self.timers[k] > 0:
                self.timers[k] -= 1
                
    def get(self, key: str) -> int:
        """Получить значение таймера."""
        return self.timers.get(key, 0)
        
    def set(self, key: str, turns: int):
        """Установить таймер."""
        self.timers[key] = turns
        
    def is_ready(self, key: str) -> bool:
        """Проверить готовность таймера."""
        return self.timers.get(key, 0) == 0
