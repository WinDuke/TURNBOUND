"""Movement and collision system."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.ecs.entity_manager import EntityManager
    from src.core.event_bus import EventBus


class MovementSystem:
    """Handles entity movement and collision detection."""

    def __init__(self, entity_manager: "EntityManager", event_bus: "EventBus"):
        self.em = entity_manager
        self.event_bus = event_bus
        self._walkable_cache: dict[tuple[int, int], bool] = {}

    def is_walkable(self, x: int, y: int, arena_map: dict) -> bool:
        """Check if a position is walkable."""
        cache_key = (x, y)
        if cache_key in self._walkable_cache:
            return self._walkable_cache[cache_key]
        
        # Check terrain
        tile = arena_map.get((x, y), {})
        terrain_type = tile.get("type", "floor")
        
        if terrain_type in ("wall", "obstacle", "water", "lava"):
            self._walkable_cache[cache_key] = False
            return False
        
        # Check for entities blocking this position
        for entity_id in self.em.get_entities_with_components("position", "renderable"):
            pos = self.em.get_component(entity_id, "position")
            if pos and pos.x == x and pos.y == y:
                # Check if entity is solid
                renderable = self.em.get_component(entity_id, "renderable")
                if renderable and not renderable.symbol.startswith("."):
                    self._walkable_cache[cache_key] = False
                    return False
        
        self._walkable_cache[cache_key] = True
        return True

    def move_entity(
        self,
        entity_id: int,
        dx: int,
        dy: int,
        arena_map: dict,
    ) -> tuple[bool, Optional[int]]:
        """
        Try to move an entity by delta.
        
        Returns (success, collided_entity_id).
        """
        position = self.em.get_component(entity_id, "position")
        faction = self.em.get_component(entity_id, "faction")
        
        if not position:
            return False, None
        
        new_x = position.x + dx
        new_y = position.y + dy
        
        # Check bounds
        if not self._is_in_bounds(new_x, new_y, arena_map):
            return False, None
        
        # Check terrain collision
        if not self.is_walkable(new_x, new_y, arena_map):
            return False, None
        
        # Check entity collision
        for other_id in self.em.get_entities_with_components("position", "faction"):
            if other_id == entity_id:
                continue
            
            other_pos = self.em.get_component(other_id, "position")
            other_faction = self.em.get_component(other_id, "faction")
            
            if other_pos and other_pos.x == new_x and other_pos.y == new_y:
                # Check if hostile
                if self._are_hostile(faction, other_faction):
                    return False, other_id
                else:
                    return False, None
        
        # Move successful
        position.x = new_x
        position.y = new_y
        
        self.event_bus.emit("move", {
            "entity_id": entity_id,
            "x": new_x,
            "y": new_y,
            "dx": dx,
            "dy": dy,
        })
        
        # Clear cache for affected tiles
        self._walkable_cache.clear()
        
        return True, None

    def teleport_entity(
        self,
        entity_id: int,
        x: int,
        y: int,
        arena_map: dict,
    ) -> bool:
        """Teleport an entity to a specific position."""
        position = self.em.get_component(entity_id, "position")
        if not position:
            return False
        
        if not self._is_in_bounds(x, y, arena_map):
            return False
        
        position.x = x
        position.y = y
        
        self._walkable_cache.clear()
        
        return True

    def get_entities_in_radius(
        self,
        x: int,
        y: int,
        radius: int,
        faction: Optional[str] = None,
    ) -> list[int]:
        """Get all entities within a radius of a position."""
        result = []
        
        for entity_id in self.em.get_entities_with_components("position"):
            pos = self.em.get_component(entity_id, "position")
            if not pos:
                continue
            
            # Check distance
            distance = abs(pos.x - x) + abs(pos.y - y)  # Manhattan distance
            if distance <= radius:
                # Check faction filter
                if faction is not None:
                    entity_faction = self.em.get_component(entity_id, "faction")
                    if not entity_faction or entity_faction.alignment != faction:
                        continue
                
                result.append(entity_id)
        
        return result

    def get_line_of_sight(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        arena_map: dict,
    ) -> bool:
        """Check if there's a clear line of sight between two points."""
        # Simple Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y2
        
        while True:
            if not self.is_walkable(x, y, arena_map):
                return False
            
            if x == x2 and y == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        return True

    def _is_in_bounds(self, x: int, y: int, arena_map: dict) -> bool:
        """Check if coordinates are within arena bounds."""
        # Find bounds from arena_map
        if not arena_map:
            return False
        
        min_x = min(k[0] for k in arena_map.keys())
        max_x = max(k[0] for k in arena_map.keys())
        min_y = min(k[1] for k in arena_map.keys())
        max_y = max(k[1] for k in arena_map.keys())
        
        return min_x <= x <= max_x and min_y <= y <= max_y

    def _are_hostile(
        self,
        faction1: Optional["Faction"],
        faction2: Optional["Faction"],
    ) -> bool:
        """Check if two factions are hostile to each other."""
        if not faction1 or not faction2:
            return False
        
        # Player and enemies are hostile
        if faction1.alignment == "player" and faction2.alignment == "enemy":
            return True
        if faction1.alignment == "enemy" and faction2.alignment == "player":
            return True
        if faction1.alignment == "boss" and faction2.alignment == "player":
            return True
        if faction1.alignment == "player" and faction2.alignment == "boss":
            return True
        
        return False
