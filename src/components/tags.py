from dataclasses import dataclass, field
from typing import Set

@dataclass
class Tags:
    """Компонент тегов для синергий и классификации."""
    values: Set[str] = field(default_factory=set)
    
    def add(self, tag: str):
        """Добавить тег."""
        self.values.add(tag)
        
    def remove(self, tag: str):
        """Удалить тег."""
        self.values.discard(tag)
        
    def has(self, tag: str) -> bool:
        """Проверить наличие тега."""
        return tag in self.values
    
    def has_any(self, tags: list) -> bool:
        """Проверить наличие любого из списка тегов."""
        return any(tag in self.values for tag in tags)
    
    def has_all(self, tags: list) -> bool:
        """Проверить наличие всех тегов из списка."""
        return all(tag in self.values for tag in tags)
    
    def clear(self):
        """Очистить все теги."""
        self.values.clear()
