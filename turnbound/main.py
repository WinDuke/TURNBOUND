"""Main game engine and application."""

import asyncio
from typing import Optional

from textual.app import App, ComposeResult
from textual.screen import Screen

from src.core.event_bus import EventBus, EVENT_KILL, EVENT_WAVE_COMPLETE
from src.ecs.entity_manager import EntityManager
from src.components import (
    Position, Renderable, Health, Energy, Stats,
    Skills, Cooldowns, AI, Statuses, Faction, Tags, Level
)
from src.generation.arena_generator import ArenaGenerator
from src.systems.combat_system import CombatSystem
from src.systems.movement_system import MovementSystem
from src.systems.ai_system import AISystem
from src.systems.wave_system import WaveSystem
from src.ui.title_screen import TitleScreen, CharacterSelectScreen
from src.ui.game_screen import GameScreen


class TurnboundApp(App):
    """Main TURNBOUND application."""

    CSS = """
    Screen {
        background: #0a0a1a;
    }
    """

    SCREENS = {
        "title": TitleScreen,
        "character_select": CharacterSelectScreen,
        "game": GameScreen,
    }

    def __init__(self):
        super().__init__()
        
        # Core systems
        self.event_bus = EventBus()
        self.entity_manager = EntityManager()
        
        # Game state
        self.arena_map = {}
        self.spawn_anchors = []
        self.player_id: Optional[int] = None
        self.current_screen: Optional[GameScreen] = None
        
        # Systems (initialized after arena)
        self.combat_system: Optional[CombatSystem] = None
        self.movement_system: Optional[MovementSystem] = None
        self.ai_system: Optional[AISystem] = None
        self.wave_system: Optional[WaveSystem] = None
        
        # Game loop
        self.turn_in_progress = False
        self.animating = False
        
        # Subscribe to events
        self._setup_event_listeners()

    def _setup_event_listeners(self) -> None:
        """Set up event bus listeners."""
        self.event_bus.subscribe(EVENT_KILL, self._on_kill)
        self.event_bus.subscribe(EVENT_WAVE_COMPLETE, self._on_wave_complete)

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.push_screen("title")

    def start_new_game(self, character_data: dict = None) -> None:
        """Start a new game session with selected character."""
        # Reset state
        self.entity_manager.clear()
        self.event_bus.clear()
        self._setup_event_listeners()
        
        # Generate arena
        generator = ArenaGenerator(width=50, height=20)
        self.arena_map, self.spawn_anchors = generator.generate("cemetery")
        
        # Create player with selected character
        char_id = character_data.get("id", "executioner") if character_data else "executioner"
        self._create_player(char_id)
        
        # Initialize systems
        self.combat_system = CombatSystem(self.entity_manager, self.event_bus)
        self.movement_system = MovementSystem(self.entity_manager, self.event_bus)
        self.ai_system = AISystem(self.entity_manager, self.event_bus)
        self.wave_system = WaveSystem(
            self.entity_manager,
            self.event_bus,
            self.arena_map,
            self.spawn_anchors,
        )
        
        # Start first wave
        self.wave_system.start_wave(1)
        
        # Push game screen
        self.current_screen = GameScreen()
        self.current_screen.set_arena(self.arena_map)
        self.push_screen(self.current_screen)
        
        # Update display
        self._update_display()

    def _create_player(self, character_id: str = "executioner") -> None:
        """Create the player entity with selected character."""
        self.player_id = self.entity_manager.create_entity()
        
        spawn_x, spawn_y = len(self.arena_map) // 2, len(self.arena_map) // 2
        
        # Character-specific data
        char_configs = {
            "executioner": {
                "symbol": "⚔",
                "color": "#ff4444",
                "hp": 120,
                "energy": 40,
                "power": 15,
                "defense": 3,
                "skills": [
                    {"id": "cleave", "name": "Cleave", "key": "Q", "range": 2, "damage": 20, "cost": 10, "cooldown": 0},
                    {"id": "hook", "name": "Chain Hook", "key": "W", "range": 6, "damage": 5, "cost": 15, "cooldown": 0},
                    {"id": "blood_surge", "name": "Blood Surge", "key": "E", "range": 1, "damage": 25, "cost": 20, "cooldown": 0},
                    {"id": "execution", "name": "Execution", "key": "R", "range": 1, "damage": 50, "cost": 30, "cooldown": 0},
                ],
            },
            "astromancer": {
                "symbol": "✦",
                "color": "#8844ff",
                "hp": 80,
                "energy": 80,
                "power": 12,
                "defense": 1,
                "skills": [
                    {"id": "star_bolt", "name": "Star Bolt", "key": "Q", "range": 8, "damage": 15, "cost": 15, "cooldown": 0},
                    {"id": "warp_step", "name": "Warp Step", "key": "W", "range": 6, "damage": 0, "cost": 20, "cooldown": 0},
                    {"id": "echo_seal", "name": "Echo Seal", "key": "E", "range": 0, "damage": 0, "cost": 25, "cooldown": 0},
                    {"id": "collapse", "name": "Collapse", "key": "R", "range": 5, "damage": 30, "cost": 40, "cooldown": 0},
                ],
            },
            "plague_saint": {
                "symbol": "☠",
                "color": "#44ff44",
                "hp": 90,
                "energy": 60,
                "power": 10,
                "defense": 2,
                "skills": [
                    {"id": "rot_touch", "name": "Rot Touch", "key": "Q", "range": 1, "damage": 12, "cost": 10, "cooldown": 0},
                    {"id": "spore_cloud", "name": "Spore Cloud", "key": "W", "range": 4, "damage": 8, "cost": 20, "cooldown": 0},
                    {"id": "harvest", "name": "Harvest", "key": "E", "range": 5, "damage": 15, "cost": 25, "cooldown": 0},
                    {"id": "bloom", "name": "Bloom", "key": "R", "range": 6, "damage": 25, "cost": 35, "cooldown": 0},
                ],
            },
            "mirror_duelist": {
                "symbol": "◊",
                "color": "#44ffff",
                "hp": 85,
                "energy": 70,
                "power": 14,
                "defense": 2,
                "crit_chance": 0.15,
                "skills": [
                    {"id": "feint", "name": "Feint", "key": "Q", "range": 1, "damage": 10, "cost": 15, "cooldown": 0},
                    {"id": "mirror_step", "name": "Mirror Step", "key": "W", "range": 5, "damage": 0, "cost": 20, "cooldown": 0},
                    {"id": "riposte", "name": "Riposte", "key": "E", "range": 0, "damage": 0, "cost": 25, "cooldown": 0},
                    {"id": "perfect_reflection", "name": "Perfect Reflection", "key": "R", "range": 0, "damage": 0, "cost": 35, "cooldown": 0},
                ],
            },
        }
        
        config = char_configs.get(character_id, char_configs["executioner"])
        
        # Add components
        self.entity_manager.add_component(
            self.player_id, "position", Position(spawn_x, spawn_y)
        )
        self.entity_manager.add_component(
            self.player_id, "renderable", Renderable(
                symbol=config["symbol"],
                color=config["color"],
                bold=True,
            )
        )
        self.entity_manager.add_component(
            self.player_id, "health", Health(current=config["hp"], max=config["hp"])
        )
        self.entity_manager.add_component(
            self.player_id, "energy", Energy(current=config["energy"], max=config["energy"])
        )
        self.entity_manager.add_component(
            self.player_id, "stats", Stats(
                power=config["power"],
                defense=config["defense"],
                crit_chance=config.get("crit_chance", 0.05),
                crit_multiplier=2.0,
            )
        )
        self.entity_manager.add_component(
            self.player_id, "skills", Skills(
                active=config["skills"]
            )
        )
        self.entity_manager.add_component(
            self.player_id, "cooldowns", Cooldowns()
        )
        self.entity_manager.add_component(
            self.player_id, "faction", Faction("player")
        )
        self.entity_manager.add_component(
            self.player_id, "level", Level()
        )
        self.entity_manager.add_component(
            self.player_id, "tags", Tags()
        )

    async def handle_input(self, action: str) -> None:
        """Handle player input actions."""
        if self.turn_in_progress or self.animating:
            return
        
        self.turn_in_progress = True
        
        try:
            if action in ("up", "down", "left", "right"):
                await self._handle_movement(action)
            elif action in ("skill_q", "skill_w", "skill_e", "skill_r"):
                await self._handle_skill(action)
            elif action == "wait":
                await self._handle_wait()
            elif action == "pause":
                await self._handle_pause()
            
            # Process enemy turns
            await self._process_enemy_turns()
            
            # Tick statuses
            await self._tick_statuses()
            
            # Check wave status
            if self.wave_system and not self.wave_system.wave_in_progress:
                self.wave_system.start_wave(self.wave_system.current_wave + 1)
            
        finally:
            self.turn_in_progress = False
            self._update_display()

    async def _handle_movement(self, direction: str) -> None:
        """Handle movement input."""
        if not self.movement_system or self.player_id is None:
            return
        
        dx, dy = 0, 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        
        success, collided_with = self.movement_system.move_entity(
            self.player_id, dx, dy, self.arena_map
        )
        
        if collided_with is not None:
            # Attack the entity we collided with
            await self._perform_attack(self.player_id, collided_with)

    async def _handle_skill(self, skill_key: str) -> None:
        """Handle skill usage input."""
        if self.player_id is None:
            return
        
        skills = self.entity_manager.get_component(self.player_id, "skills")
        cooldowns = self.entity_manager.get_component(self.player_id, "cooldowns")
        energy = self.entity_manager.get_component(self.player_id, "energy")
        
        if not skills or not cooldowns or not energy:
            return
        
        # Find skill by key
        skill_map = {"skill_q": "Q", "skill_w": "W", "skill_e": "E", "skill_r": "R"}
        key = skill_map.get(skill_key)
        
        for skill in skills.active:
            if skill.get("key") == key:
                skill_id = skill.get("id")
                
                # Check cooldown
                if not cooldowns.is_ready(skill_id):
                    if self.current_screen:
                        self.current_screen.log_combat(f"{skill['name']} on cooldown!", "yellow")
                    return
                
                # Check energy
                cost = skill.get("cost", 0)
                if energy.current < cost:
                    if self.current_screen:
                        self.current_screen.log_combat("Not enough energy!", "yellow")
                    return
                
                # Use skill
                energy.spend(cost)
                cooldowns.add(skill_id, 3)  # Default 3 turn cooldown
                
                if self.current_screen:
                    self.current_screen.log_combat(f"Used {skill['name']}!", "bold green")
                
                # Apply skill effect (simplified for MVP)
                if skill.get("damage", 0) > 0:
                    # Find nearest enemy
                    nearest = self._find_nearest_enemy()
                    if nearest:
                        result = self.combat_system.calculate_damage(
                            self.player_id, nearest, skill["damage"]
                        )
                        self.combat_system.apply_damage(nearest, result["damage"])
                        
                        if self.current_screen:
                            style = "bold red" if result["is_crit"] else "red"
                            self.current_screen.log_combat(
                                f"Hit enemy for {result['damage']} damage!", style
                            )
                break

    async def _handle_wait(self) -> None:
        """Handle wait/skip turn action."""
        if self.current_screen:
            self.current_screen.log_combat("Waiting...", "dim")

    async def _handle_pause(self) -> None:
        """Handle pause action."""
        # TODO: Implement pause menu
        pass

    async def _perform_attack(self, attacker_id: int, target_id: int) -> None:
        """Perform a basic attack."""
        if not self.combat_system:
            return
        
        result = self.combat_system.calculate_damage(
            attacker_id, target_id, base_damage=10
        )
        
        actual_damage = self.combat_system.apply_damage(
            target_id, result["damage"]
        )
        
        if self.current_screen:
            if result["is_crit"]:
                self.current_screen.log_combat(
                    f"Critical hit! {actual_damage} damage!", "bold red"
                )
            else:
                self.current_screen.log_combat(
                    f"Hit for {actual_damage} damage.", "red"
                )

    async def _process_enemy_turns(self) -> None:
        """Process all enemy AI turns."""
        if not self.ai_system or not self.movement_system:
            return
        
        for entity_id in self.entity_manager.get_entities_with_components("ai", "faction"):
            faction = self.entity_manager.get_component(entity_id, "faction")
            if faction and faction.alignment == "enemy":
                # Decide action
                decision = self.ai_system.decide_action(entity_id, self.player_id)
                
                if decision.action == "attack" and decision.target_id:
                    await self._perform_attack(entity_id, decision.target_id)
                elif decision.action == "move_to_target" and decision.target_id:
                    # Move toward player
                    target_pos = self.entity_manager.get_component(decision.target_id, "position")
                    if target_pos:
                        entity_pos = self.entity_manager.get_component(entity_id, "position")
                        if entity_pos:
                            dx = 1 if target_pos.x > entity_pos.x else (-1 if target_pos.x < entity_pos.x else 0)
                            dy = 1 if target_pos.y > entity_pos.y else (-1 if target_pos.y < entity_pos.y else 0)
                            self.movement_system.move_entity(entity_id, dx, dy, self.arena_map)

    async def _tick_statuses(self) -> None:
        """Tick all status effects."""
        if not self.combat_system:
            return
        
        for entity_id in self.entity_manager.get_all_entities():
            self.combat_system.tick_statuses(entity_id)
        
        # Tick cooldowns
        for entity_id in self.entity_manager.get_entities_with_components("cooldowns"):
            cooldowns = self.entity_manager.get_component(entity_id, "cooldowns")
            if cooldowns:
                cooldowns.tick()
        
        # Regenerate energy
        for entity_id in self.entity_manager.get_entities_with_components("energy"):
            energy = self.entity_manager.get_component(entity_id, "energy")
            if energy:
                energy.restore(energy.regen)

    def _find_nearest_enemy(self) -> Optional[int]:
        """Find the nearest enemy to the player."""
        if self.player_id is None:
            return None
        
        player_pos = self.entity_manager.get_component(self.player_id, "position")
        if not player_pos:
            return None
        
        nearest = None
        nearest_dist = float('inf')
        
        for entity_id in self.entity_manager.get_entities_with_components("position", "faction"):
            faction = self.entity_manager.get_component(entity_id, "faction")
            if faction and faction.alignment == "enemy":
                pos = self.entity_manager.get_component(entity_id, "position")
                if pos:
                    dist = abs(pos.x - player_pos.x) + abs(pos.y - player_pos.y)
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest = entity_id
        
        return nearest

    def _on_kill(self, data: dict) -> None:
        """Handle kill event."""
        victim_id = data.get("victim_id")
        killer_id = data.get("killer_id")
        
        if victim_id is not None:
            # Check if enemy
            faction = self.entity_manager.get_component(victim_id, "faction")
            if faction and faction.alignment == "enemy":
                # Award EXP
                if self.player_id and killer_id == self.player_id:
                    level = self.entity_manager.get_component(self.player_id, "level")
                    if level:
                        leveled_up = level.add_exp(20)
                        if self.current_screen:
                            self.current_screen.log_combat("+20 EXP", "yellow")
                            if leveled_up:
                                self.current_screen.log_combat("LEVEL UP!", "bold yellow")
                
                # Notify wave system
                if self.wave_system:
                    self.wave_system.on_enemy_death(victim_id)
            
            # Remove entity
            self.entity_manager.destroy_entity(victim_id)

    def _on_wave_complete(self, data: dict) -> None:
        """Handle wave complete event."""
        wave_number = data.get("wave_number")
        
        if self.current_screen:
            self.current_screen.log_combat(
                f"Wave {wave_number} complete!", "bold green"
            )

    def _update_display(self) -> None:
        """Update the game display."""
        if not self.current_screen:
            return
        
        # Get all entities with position and renderable
        entities = []
        for entity_id in self.entity_manager.get_entities_with_components("position", "renderable"):
            entity_data = {
                "id": entity_id,
                "position": self.entity_manager.get_component(entity_id, "position"),
                "renderable": self.entity_manager.get_component(entity_id, "renderable"),
                "health": self.entity_manager.get_component(entity_id, "health"),
                "faction": self.entity_manager.get_component(entity_id, "faction"),
            }
            entities.append(entity_data)
        
        self.current_screen.set_entities(entities)
        
        # Update game state
        player = self.entity_manager.get_component(self.player_id, "health") if self.player_id else None
        energy = self.entity_manager.get_component(self.player_id, "energy") if self.player_id else None
        skills = self.entity_manager.get_component(self.player_id, "skills") if self.player_id else None
        
        self.current_screen.game_state = {
            "player": {
                "hp": player.current if player else 100,
                "max_hp": player.max if player else 100,
                "energy": energy.current if energy else 50,
                "max_energy": energy.max if energy else 50,
                "skills": skills.active if skills else [],
            },
            "wave": self.wave_system.current_wave if self.wave_system else 1,
            "enemies_remaining": self.wave_system.enemies_remaining if self.wave_system else 0,
        }


def main():
    """Entry point for the game."""
    app = TurnboundApp()
    app.run()


if __name__ == "__main__":
    main()
