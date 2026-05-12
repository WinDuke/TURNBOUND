from dataclasses import dataclass

@dataclass
class Position:
    """Компонент позиции сущности на сетке."""
    x: int
    y: int
