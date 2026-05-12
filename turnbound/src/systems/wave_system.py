"""Wave management and enemy spawning system."""

import random
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.ecs.entity_manager import EntityManager
    from src.core.event_bus import EventBus


class WaveSystem:
    """Manages enemy waves and difficulty scaling."""

    def __init__(
        self,
        entity_manager: "EntityManager",
        event_bus: "EventBus",
        arena_map: dict,
        spawn_anchors: list[tuple[int, int]],
    ):
        self.em = entity_manager
        self.event_bus = event_bus
        self.arena_map = arena_map
        self.spawn_anchors = spawn_anchors
        
        self.current_wave = 0
        self.wave_in_progress = False
        self.enemies_remaining = 0
        self.threat_budget = 0
        self.boss_wave_interval = 5  # Boss every 5 waves

    def start_wave(self, wave_number: int) -> None:
        """Start a new wave with calculated threat budget."""
        self.current_wave = wave_number
        self.wave_in_progress = True
        
        # Calculate threat budget
        base_budget = 10
        scaling = 1.5
        self.threat_budget = int(base_budget * (scaling ** (wave_number - 1)))
        
        # Check if this is a boss wave
        if wave_number > 0 and wave_number % self.boss_wave_interval == 0:
            self._start_boss_wave()
        else:
            self._spawn_normal_wave()

    def _start_boss_wave(self) -> None:
        """Start a boss wave - clear normal enemies first."""
        # Clear all normal enemies
        for entity_id in list(self.em.get_all_entities()):
            faction = self.em.get_component(entity_id, "faction")
            if faction and faction.alignment == "enemy":
                self.em.destroy_entity(entity_id)
        
        # Boss will be spawned by boss system
        self.threat_budget = 0  # No additional enemies during boss
        self.enemies_remaining = 1  # Just the boss

    def _spawn_normal_wave(self) -> None:
        """Spawn enemies based on threat budget."""
        budget = self.threat_budget
        enemies_spawned = 0
        
        # Enemy templates with costs
        enemy_templates = [
            ("zombie", 2),
            ("skeleton", 3),
            ("spitter", 4),
            ("knight", 6),
            ("necromancer", 10),
        ]
        
        while budget >= 2:  # Minimum cost is 2
            # Choose enemy based on remaining budget
            available = [t for t in enemy_templates if t[1] <= budget]
            if not available:
                break
            
            # Weight toward cheaper enemies early, expensive later
            wave_factor = min(1.0, self.current_wave / 10)
            weights = [1.0 - (t[1] / 10) * (1 - wave_factor) for t in available]
            
            chosen = random.choices(available, weights=weights)[0]
            budget -= chosen[1]
            
            # Spawn enemy
            self._spawn_enemy(chosen[0])
            enemies_spawned += 1
        
        self.enemies_remaining = enemies_spawned

    def _spawn_enemy(self, enemy_type: str) -> Optional[int]:
        """Spawn an enemy at a random spawn anchor."""
        if not self.spawn_anchors:
            return None
        
        anchor = random.choice(self.spawn_anchors)
        x, y = anchor
        
        # Find valid spawn position near anchor
        spawn_pos = self._find_valid_spawn(x, y)
        if not spawn_pos:
            return None
        
        # Create entity
        entity_id = self.em.create_entity()
        
        # Get enemy data
        enemy_data = self._get_enemy_data(enemy_type)
        
        # Add components
        from src.components import Position, Renderable, Health, Stats, AI, Faction, Skills, Cooldowns
        
        self.em.add_component(entity_id, "position", Position(spawn_pos[0], spawn_pos[1]))
        self.em.add_component(entity_id, "renderable", Renderable(
            symbol=enemy_data["symbol"],
            color=enemy_data.get("color", "#ff4444"),
        ))
        self.em.add_component(entity_id, "health", Health(
            current=enemy_data["health"],
            max=enemy_data["health"],
        ))
        self.em.add_component(entity_id, "stats", Stats(
            power=enemy_data.get("power", 5),
            defense=enemy_data.get("defense", 0),
        ))
        self.em.add_component(entity_id, "ai", AI(
            behavior_type=enemy_data.get("behavior", "aggressive"),
        ))
        self.em.add_component(entity_id, "faction", Faction("enemy"))
        
        if enemy_data.get("skills"):
            self.em.add_component(entity_id, "skills", Skills(active=enemy_data["skills"]))
            self.em.add_component(entity_id, "cooldowns", Cooldowns())
        
        self.enemies_remaining += 1
        
        return entity_id

    def _find_valid_spawn(self, center_x: int, center_y: int, radius: int = 3) -> Optional[tuple[int, int]]:
        """Find a valid spawn position near the center point."""
        positions = []
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = center_x + dx
                y = center_y + dy
                
                tile = self.arena_map.get((x, y), {})
                if tile.get("type") == "floor":
                    # Check no entity here
                    blocked = False
                    for entity_id in self.em.get_entities_with_components("position"):
                        pos = self.em.get_component(entity_id, "position")
                        if pos and pos.x == x and pos.y == y:
                            blocked = True
                            break
                    
                    if not blocked:
                        positions.append((x, y))
        
        if positions:
            return random.choice(positions)
        return None

    def _get_enemy_data(self, enemy_type: str) -> dict:
        """Get enemy template data."""
        templates = {
            "zombie": {
                "symbol": "z",
                "color": "#88aa88",
                "health": 20,
                "power": 3,
                "defense": 0,
                "behavior": "aggressive",
            },
            "skeleton": {
                "symbol": "s",
                "color": "#cccccc",
                "health": 15,
                "power": 5,
                "defense": 0,
                "behavior": "tactical",
            },
            "spitter": {
                "symbol": "p",
                "color": "#00ff00",
                "health": 12,
                "power": 4,
                "defense": 0,
                "behavior": "defensive",
                "skills": [{"id": "spit", "name": "Spit", "range": 5, "damage": 8, "cost": 0, "cooldown": 3}],
            },
            "knight": {
                "symbol": "K",
                "color": "#aaaaaa",
                "health": 40,
                "power": 6,
                "defense": 3,
                "behavior": "defensive",
            },
            "necromancer": {
                "symbol": "N",
                "color": "#aa00ff",
                "health": 25,
                "power": 8,
                "defense": 0,
                "behavior": "tactical",
                "skills": [{"id": "dark_bolt", "name": "Dark Bolt", "range": 4, "damage": 10, "cost": 0, "cooldown": 2}],
            },
        }
        
        return templates.get(enemy_type, templates["zombie"])

    def on_enemy_death(self, enemy_id: int) -> None:
        """Called when an enemy dies."""
        self.enemies_remaining = max(0, self.enemies_remaining - 1)
        
        # Check if wave complete
        if self.enemies_remaining == 0 and self.wave_in_progress:
            self._complete_wave()

    def _complete_wave(self) -> None:
        """Mark current wave as complete."""
        self.wave_in_progress = False
        
        self.event_bus.emit("wave_complete", {
            "wave_number": self.current_wave,
        })

    def get_wave_info(self) -> dict:
        """Get current wave information."""
        return {
            "wave": self.current_wave,
            "in_progress": self.wave_in_progress,
            "enemies_remaining": self.enemies_remaining,
            "threat_budget": self.threat_budget,
            "next_boss_wave": self.boss_wave_interval - (self.current_wave % self.boss_wave_interval),
        }
