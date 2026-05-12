from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class AI:
    """Компонент искусственного интеллекта сущности."""
    behavior_type: str = "aggressive"
    params: Dict[str, Any] = field(default_factory=dict)
    
    # Параметры для различных поведений
    # aggressive: prioritizes attack
    # defensive: prioritizes defense
    # tactical: uses skills strategically
    # coward: retreats on low HP
    
    def get_param(self, key: str, default: Any = None) -> Any:
        """Получить параметр поведения."""
        return self.params.get(key, default)
        
    def set_param(self, key: str, value: Any):
        """Установить параметр поведения."""
        self.params[key] = value
