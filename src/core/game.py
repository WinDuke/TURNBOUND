"""
TURNBOUND - Game Engine Core
Main game loop and state management
"""

import asyncio
from typing import Dict, Any, Optional, List

from src.core.constants import STATE_MENU, STATE_PLAYING, STATE_BOSS, STATE_GAMEOVER, STATE_PAUSED, STATE_LEVELUP
from src.core.event_bus import EventBus
from src.ecs.entity_manager import EntityManager


class GameEngine:
    """
    Main game engine controller
    Manages game state, systems, and turn flow
    """
    
    def __init__(self):
        self.entities = EntityManager()
        self.events = EventBus()
        
        # Systems (initialized later)
        self.combat_system = None
        self.movement_system = None
        self.ai_system = None
        self.wave_system = None
        self.status_system = None
        self.level_system = None
        self.render_system = None
        self.upgrade_system = None
        self.boss_system = None
        
        # Game State
        self.state = STATE_MENU
        self.current_arena: Optional[Dict[str, Any]] = None
        self.player_id: Optional[int] = None
        self.turn_count: int = 0
        self.current_wave: int = 0
        
        # Input buffer
        self.input_queue: List[Dict[str, Any]] = []
        
        # Animation queue
        self.animation_queue: List[Dict[str, Any]] = []
    
    def initialize_systems(self, systems: Dict[str, Any]) -> None:
        """Initialize all game systems"""
        for name, system in systems.items():
            setattr(self, name, system)
    
    def init_game(self, character_id: str, arena_data: Dict[str, Any]) -> None:
        """Initialize a new game session"""
        self.entities.clear()
        self.events.clear()
        self.turn_count = 0
        self.current_wave = 1
        self.input_queue.clear()
        self.animation_queue.clear()
        
        # Set arena
        self.current_arena = arena_data
        
        # State
        self.state = STATE_PLAYING
    
    def start_turn(self) -> None:
        """Begin player turn"""
        pass
    
    def process_action(self, action_type: str, data: Dict[str, Any]) -> bool:
        """
        Process a player action
        Returns True if action was valid and turn should advance
        """
        if self.state not in [STATE_PLAYING, STATE_BOSS]:
            return False
        
        if not self.player_id or not self.entities.entity_exists(self.player_id):
            return False
        
        success = False
        
        if action_type == "MOVE":
            if self.movement_system:
                dx = data.get("dx", 0)
                dy = data.get("dy", 0)
                success = self.movement_system.move_entity(self.player_id, dx, dy)
        
        elif action_type == "SKILL":
            if self.combat_system:
                skill_id = data.get("skill_id")
                target = data.get("target")
                success = self.combat_system.use_skill(self.player_id, skill_id, target)
        
        elif action_type == "WAIT":
            success = True  # Wait always succeeds
        
        elif action_type == "INTERACT":
            # TODO: Implement interaction
            success = False
        
        if success:
            self._trigger_event("player_action", {"type": action_type, "data": data})
        
        return success
    
    def end_turn(self) -> None:
        """Process end of turn: enemies, statuses, waves"""
        # 1. Tick cooldowns for player
        player_skills = self.entities.get_component(self.player_id, "Skills")
        if player_skills:
            player_skills.tick_cooldowns()
        
        # 2. Status ticks for all entities
        if self.status_system:
            self.status_system.tick_all()
        
        # 3. Enemy turns
        if self.ai_system:
            self.ai_system.process_all_enemies()
        
        # 4. Wave logic
        if self.wave_system:
            self.wave_system.update()
        
        # 5. Boss logic
        if self.boss_system and self.state == STATE_BOSS:
            self.boss_system.update()
        
        # 6. Increment turn counter
        self.turn_count += 1
        
        # 7. Trigger turn end event
        self._trigger_event("turn_end", {"turn": self.turn_count})
    
    def _trigger_event(self, event_name: str, data: Any = None) -> None:
        """Trigger an event through the event bus"""
        self.events.trigger(event_name, data)
    
    def set_state(self, new_state: str) -> None:
        """Change game state"""
        old_state = self.state
        self.state = new_state
        self._trigger_event("state_change", {"old": old_state, "new": new_state})
    
    def get_player_health(self) -> tuple:
        """Get player current/max HP"""
        if not self.player_id:
            return (0, 0)
        health = self.entities.get_component(self.player_id, "Health")
        if health:
            return (health.current_hp, health.max_hp)
        return (0, 0)
    
    def get_player_energy(self) -> tuple:
        """Get player current/max energy"""
        if not self.player_id:
            return (0, 0)
        energy = self.entities.get_component(self.player_id, "Energy")
        if energy:
            return (energy.current, energy.max_energy)
        return (0, 0)
    
    def is_player_alive(self) -> bool:
        """Check if player is alive"""
        if not self.player_id:
            return False
        health = self.entities.get_component(self.player_id, "Health")
        return health is not None and not health.is_dead()
    
    def check_game_over(self) -> bool:
        """Check if game over conditions are met"""
        if not self.is_player_alive():
            self.set_state(STATE_GAMEOVER)
            return True
        return False
    
    def subscribe(self, event_name: str, callback) -> None:
        """Subscribe to a game event"""
        self.events.subscribe(event_name, callback)
    
    def get_turn_count(self) -> int:
        """Get current turn number"""
        return self.turn_count
    
    def get_wave_number(self) -> int:
        """Get current wave number"""
        return self.current_wave
