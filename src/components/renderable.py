from dataclasses import dataclass

@dataclass
class Renderable:
    """Компонент отображения сущности."""
    symbol: str
    color: str
    bg_color: str = "default"
    layer: int = 2  # 0=terrain, 1=objects, 2=units, 3=effects
    
    # Дополнительные визуальные эффекты
    bold: bool = False
    dim: bool = False
    blink: bool = False
    reverse: bool = False
    underline: bool = False
    
    def get_style(self) -> str:
        """Получить Rich стиль для отрисовки."""
        parts = []
        if self.bold:
            parts.append("bold")
        if self.dim:
            parts.append("dim")
        if self.blink:
            parts.append("blink")
        if self.reverse:
            parts.append("reverse")
        if self.underline:
            parts.append("underline")
        
        style = self.color
        if parts:
            style = f"{' '.join(parts)} {self.color}"
        
        return style
    
    def to_rich_string(self) -> str:
        """Преобразовать в строку Rich формата."""
        style = self.get_style()
        return f"[{style}]{self.symbol}[/]"
