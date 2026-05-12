from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Skills:
    """Компонент известных навыков и их кулдаунов."""
    known: List[str] = field(default_factory=list)
    cooldowns: Dict[str, int] = field(default_factory=dict)
    
    def add_skill(self, skill_id: str):
        """Добавить навык."""
        if skill_id not in self.known:
            self.known.append(skill_id)
            self.cooldowns[skill_id] = 0
            
    def tick_cooldowns(self):
        """Уменьшить кулдауны на 1."""
        for k in list(self.cooldowns.keys()):
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1
                
    def can_use(self, skill_id: str) -> bool:
        """Проверить, можно ли использовать навык."""
        return skill_id in self.known and self.cooldowns.get(skill_id, 0) == 0
    
    def set_cooldown(self, skill_id: str, turns: int):
        """Установить кулдаун для навыка."""
        if skill_id in self.known:
            self.cooldowns[skill_id] = turns
