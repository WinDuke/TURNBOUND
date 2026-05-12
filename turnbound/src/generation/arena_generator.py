"""Procedural arena generation."""

import random
from typing import Optional


class ArenaGenerator:
    """Generates procedural arena maps."""

    def __init__(self, width: int = 50, height: int = 20):
        self.width = width
        self.height = height
        self.arena_map: dict[tuple[int, int], dict] = {}
        self.spawn_anchors: list[tuple[int, int]] = []
        self.biome_type = "cemetery"

    def generate(self, biome: str = "cemetery") -> tuple[dict, list[tuple[int, int]]]:
        """Generate a new arena map."""
        self.biome_type = biome
        self.arena_map = {}
        self.spawn_anchors = []
        
        # Initialize all tiles as floor
        for x in range(self.width):
            for y in range(self.height):
                self.arena_map[(x, y)] = {
                    "type": "floor",
                    "symbol": ".",
                    "color": "#444444",
                }
        
        # Generate borders
        self._generate_borders()
        
        # Generate obstacles based on biome
        self._generate_obstacles()
        
        # Generate biome-specific features
        if biome == "cemetery":
            self._generate_cemetery_features()
        elif biome == "crimson_cathedral":
            self._generate_cathedral_features()
        elif biome == "frozen_hollow":
            self._generate_frozen_features()
        elif biome == "void_fracture":
            self._generate_void_features()
        
        # Place spawn anchors
        self._place_spawn_anchors()
        
        return self.arena_map, self.spawn_anchors

    def _generate_borders(self) -> None:
        """Generate arena borders."""
        for x in range(self.width):
            # Top and bottom borders
            self.arena_map[(x, 0)] = {"type": "wall", "symbol": "#", "color": "#666666"}
            self.arena_map[(x, self.height - 1)] = {"type": "wall", "symbol": "#", "color": "#666666"}
        
        for y in range(self.height):
            # Left and right borders
            self.arena_map[(0, y)] = {"type": "wall", "symbol": "#", "color": "#666666"}
            self.arena_map[(self.width - 1, y)] = {"type": "wall", "symbol": "#", "color": "#666666"}

    def _generate_obstacles(self) -> None:
        """Generate random obstacles."""
        num_obstacles = (self.width * self.height) // 30
        
        for _ in range(num_obstacles):
            x = random.randint(3, self.width - 4)
            y = random.randint(3, self.height - 4)
            
            # Don't place in center area (player spawn zone)
            center_x = self.width // 2
            center_y = self.height // 2
            if abs(x - center_x) < 5 and abs(y - center_y) < 5:
                continue
            
            self.arena_map[(x, y)] = {
                "type": "obstacle",
                "symbol": "▓",
                "color": "#777777",
            }

    def _generate_cemetery_features(self) -> None:
        """Generate cemetery biome features."""
        # Add tombstones
        num_tombstones = (self.width * self.height) // 50
        
        for _ in range(num_tombstones):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            if self.arena_map[(x, y)]["type"] == "floor":
                self.arena_map[(x, y)] = {
                    "type": "obstacle",
                    "symbol": "†",
                    "color": "#888899",
                }
        
        # Add fog patches
        num_fog = (self.width * self.height) // 40
        
        for _ in range(num_fog):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            tile = self.arena_map[(x, y)]
            if tile["type"] == "floor":
                tile["bg_color"] = "#2a2a2a"

    def _generate_cathedral_features(self) -> None:
        """Generate crimson cathedral biome features."""
        # Add pillars
        pillar_positions = [
            (self.width // 4, self.height // 2),
            (3 * self.width // 4, self.height // 2),
        ]
        
        for px, py in pillar_positions:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x, y = px + dx, py + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.arena_map[(x, y)] = {
                            "type": "obstacle",
                            "symbol": "█",
                            "color": "#662222",
                        }
        
        # Add blood pools
        num_pools = (self.width * self.height) // 60
        
        for _ in range(num_pools):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            tile = self.arena_map[(x, y)]
            if tile["type"] == "floor":
                tile["type"] = "hazard"
                tile["symbol"] = "≈"
                tile["color"] = "#cc0000"

    def _generate_frozen_features(self) -> None:
        """Generate frozen hollow biome features."""
        # Add ice patches
        num_ice = (self.width * self.height) // 30
        
        for _ in range(num_ice):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            tile = self.arena_map[(x, y)]
            if tile["type"] == "floor":
                tile["symbol"] = "*"
                tile["color"] = "#aaddff"

    def _generate_void_features(self) -> None:
        """Generate void fracture biome features."""
        # Add void anomalies
        num_anomalies = (self.width * self.height) // 40
        
        for _ in range(num_anomalies):
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            
            tile = self.arena_map[(x, y)]
            if tile["type"] == "floor":
                tile["bg_color"] = "#330055"
                tile["symbol"] = "░"

    def _place_spawn_anchors(self) -> None:
        """Place enemy spawn anchors around the arena edges."""
        margin = 3
        
        # Top edge
        for x in range(margin, self.width - margin, 8):
            self.spawn_anchors.append((x, margin))
        
        # Bottom edge
        for x in range(margin, self.width - margin, 8):
            self.spawn_anchors.append((x, self.height - margin - 1))
        
        # Left edge
        for y in range(margin, self.height - margin, 6):
            self.spawn_anchors.append((margin, y))
        
        # Right edge
        for y in range(margin, self.height - margin, 6):
            self.spawn_anchors.append((self.width - margin - 1, y))

    def get_player_spawn(self) -> tuple[int, int]:
        """Get the player spawn position (center of arena)."""
        return (self.width // 2, self.height // 2)

    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a position is walkable."""
        tile = self.arena_map.get((x, y), {})
        return tile.get("type") not in ("wall", "obstacle")
