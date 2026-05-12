"""Core game state management."""

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class GameState:
    """Central game state container."""
    
    # Game flow
    current_state: str = "title"  # title, playing, paused, levelup, gameover, boss_intro
    turn_number: int = 0
    is_player_turn: bool = True
    
    # Arena
    arena_map: dict = field(default_factory=dict)
    spawn_anchors: list = field(default_factory=list)
    
    # Entities
    player_id: Optional[int] = None
    
    # Wave progression
    current_wave: int = 0
    wave_in_progress: bool = False
    enemies_remaining: int = 0
    
    # Boss state
    boss_active: bool = False
    boss_id: Optional[int] = None
    boss_phase: int = 1
    
    # Level up state
    pending_levelup: bool = False
    upgrade_choices: list = field(default_factory=list)
    
    # Combat log buffer
    combat_log: list = field(default_factory=list)
    
    def add_log(self, message: str, style: str = "") -> None:
        """Add a message to the combat log."""
        self.combat_log.append((message, style))
        if len(self.combat_log) > 50:  # Keep last 50 messages
            self.combat_log.pop(0)
    
    def start_boss_fight(self, boss_id: int) -> None:
        """Start a boss fight."""
        self.boss_active = True
        self.boss_id = boss_id
        self.boss_phase = 1
    
    def end_boss_fight(self) -> None:
        """End the boss fight."""
        self.boss_active = False
        self.boss_id = None
        self.boss_phase = 1
    
    def next_boss_phase(self) -> None:
        """Advance to next boss phase."""
        self.boss_phase += 1


# State transitions
STATE_TITLE = "title"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_LEVELUP = "levelup"
STATE_GAMEOVER = "gameover"
STATE_BOSS_INTRO = "boss_intro"
