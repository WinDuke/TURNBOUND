from dataclasses import dataclass, field
from typing import List

@dataclass
class StatusEffect:
    """Представление активного статус-эффекта."""
    id: str
    duration: int
    stacks: int = 1
    source_id: int = 0  # Кто наложил эффект

@dataclass
class Statuses:
    """Компонент активных статус-эффектов сущности."""
    active: List[StatusEffect] = field(default_factory=list)
    
    def add(self, effect: StatusEffect) -> bool:
        """Добавить статус-эффект. Возвращает True если добавлен успешно."""
        # Проверка на существующий эффект
        existing = next((s for s in self.active if s.id == effect.id), None)
        if existing:
            # Обновление длительности и стаков
            existing.duration = max(existing.duration, effect.duration)
            existing.stacks += effect.stacks
            return True
        else:
            self.active.append(effect)
            return True
            
    def remove(self, effect_id: str) -> bool:
        """Удалить статус-эффект по ID."""
        for i, s in enumerate(self.active):
            if s.id == effect_id:
                self.active.pop(i)
                return True
        return False
        
    def get(self, effect_id: str) -> StatusEffect:
        """Получить статус-эффект по ID."""
        return next((s for s in self.active if s.id == effect_id), None)
        
    def has(self, effect_id: str) -> bool:
        """Проверить наличие статус-эффекта."""
        return any(s.id == effect_id for s in self.active)
    
    def tick(self) -> List[StatusEffect]:
        """Уменьшить длительность всех эффектов на 1. Возвращает список истекших."""
        expired = []
        for s in self.active:
            s.duration -= 1
            if s.duration <= 0:
                expired.append(s)
        
        # Удаление истекших
        for s in expired:
            if s in self.active:
                self.active.remove(s)
                
        return expired
    
    def clear(self):
        """Очистить все эффекты."""
        self.active.clear()
