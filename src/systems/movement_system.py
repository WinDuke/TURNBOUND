from typing import Tuple

class MovementSystem:
    """Система перемещения сущностей по сетке."""
    
    def __init__(self, engine):
        self.engine = engine
        
    def move_entity(
        self, 
        entity_id: int, 
        dx: int, 
        dy: int
    ) -> Tuple[bool, str]:
        """
        Переместить сущность на (dx, dy).
        Возвращает (success, reason).
        """
        pos = self.engine.entities.get_component(entity_id, "Position")
        if not pos:
            return False, "no_position_component"
        
        new_x = pos.x + dx
        new_y = pos.y + dy
        
        # Проверка границ арены
        arena = self.engine.current_arena
        if not arena:
            return False, "no_arena"
        
        if not (0 <= new_x < arena["width"] and 0 <= new_y < arena["height"]):
            return False, "out_of_bounds"
        
        # Проверка коллизий с terrain
        tile = arena["grid"][new_y][new_x]
        if self._is_solid_tile(tile):
            return False, "solid_tile"
        
        # Проверка коллизий с другими сущностями
        collision = self._check_entity_collision(entity_id, new_x, new_y)
        if collision:
            return False, f"blocked_by_{collision}"
        
        # Применение перемещения
        pos.x = new_x
        pos.y = new_y
        
        # Событие перемещения
        self.engine.events.trigger("on_move", {
            "entity": entity_id,
            "x": new_x,
            "y": new_y,
            "dx": dx,
            "dy": dy
        })
        
        return True, "success"
    
    def _is_solid_tile(self, tile: str) -> bool:
        """Проверить, является ли клетка твердой."""
        solid_tiles = ["#", "█", "▓", "▒", "░"]
        return tile in solid_tiles
    
    def _check_entity_collision(
        self, 
        exclude_id: int, 
        x: int, 
        y: int
    ) -> int:
        """
        Проверить наличие сущности в клетке.
        Возвращает ID сущности или None.
        """
        entities = self.engine.entities.query_components(["Position"])
        
        for eid in entities:
            if eid == exclude_id:
                continue
            
            pos = self.engine.entities.get_component(eid, "Position")
            if pos and pos.x == x and pos.y == y:
                return eid
        
        return None
    
    def can_move_to(
        self, 
        entity_id: int, 
        x: int, 
        y: int
    ) -> Tuple[bool, str]:
        """
        Проверить возможность перемещения в указанную клетку.
        """
        pos = self.engine.entities.get_component(entity_id, "Position")
        if not pos:
            return False, "no_position"
        
        arena = self.engine.current_arena
        if not arena:
            return False, "no_arena"
        
        # Границы
        if not (0 <= x < arena["width"] and 0 <= y < arena["height"]):
            return False, "out_of_bounds"
        
        # Terrain
        tile = arena["grid"][y][x]
        if self._is_solid_tile(tile):
            return False, "solid_tile"
        
        # Entities
        if self._check_entity_collision(entity_id, x, y):
            return False, "blocked"
        
        return True, "clear"
    
    def get_distance(
        self, 
        entity_a: int, 
        entity_b: int
    ) -> int:
        """Получить расстояние между двумя сущностями (Manhattan)."""
        pos_a = self.engine.entities.get_component(entity_a, "Position")
        pos_b = self.engine.entities.get_component(entity_b, "Position")
        
        if not pos_a or not pos_b:
            return float('inf')
        
        return abs(pos_a.x - pos_b.x) + abs(pos_a.y - pos_b.y)
    
    def is_adjacent(self, entity_a: int, entity_b: int) -> bool:
        """Проверить, являются ли две сущности соседними."""
        return self.get_distance(entity_a, entity_b) == 1
