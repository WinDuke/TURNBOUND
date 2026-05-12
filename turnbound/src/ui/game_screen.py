"""Main game screen with arena rendering and UI."""

from textual.app import Screen
from textual.widgets import Static, Label
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import asyncio

from src.core.constants import (
    ARENA_WIDTH, ARENA_HEIGHT,
    COLOR_PLAYER, COLOR_ENEMY, COLOR_BOSS,
    COLOR_HEALTH_HIGH, COLOR_HEALTH_MED, COLOR_HEALTH_LOW,
    COLOR_ENERGY,
)
from src.render.symbols import get_symbol, get_palette


class ArenaDisplay(Static):
    """Widget that renders the game arena."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arena_map = {}
        self.entities = []
        self.camera_x = 0
        self.camera_y = 0

    def render(self) -> Text:
        """Render the arena to a Rich Text object."""
        text = Text()
        
        # Get visible area based on camera
        view_width = min(ARENA_WIDTH, 50)
        view_height = min(ARENA_HEIGHT, 20)
        
        start_x = max(0, self.camera_x - view_width // 2)
        start_y = max(0, self.camera_y - view_height // 2)
        end_x = min(start_x + view_width, ARENA_WIDTH)
        end_y = min(start_y + view_height, ARENA_HEIGHT)
        
        # Build entity lookup for fast access
        entity_map = {}
        for entity in self.entities:
            pos = entity.get("position")
            if pos:
                entity_map[(pos.x, pos.y)] = entity
        
        # Render each tile
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                # Check for entity first
                entity = entity_map.get((x, y))
                if entity:
                    renderable = entity.get("renderable")
                    if renderable:
                        style = f"{renderable.color}"
                        if renderable.bold:
                            style += " bold"
                        if renderable.blink:
                            style += " blink"
                        text.append(renderable.symbol, style=style)
                        continue
                
                # Render terrain
                tile = self.arena_map.get((x, y), {})
                symbol = tile.get("symbol", ".")
                color = tile.get("color", "#444444")
                bg_color = tile.get("bg_color")
                
                style = color
                if bg_color:
                    style = f"{color} on {bg_color}"
                
                text.append(symbol, style=style)
            
            text.append("\n")
        
        return text


class HUD(Static):
    """Heads-up display widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_energy = 50
        self.player_max_energy = 50
        self.skills = []
        self.wave = 1
        self.enemies_remaining = 0

    def render(self) -> Panel:
        """Render the HUD panel."""
        # Health bar
        hp_percent = self.player_hp / self.player_max_hp if self.player_max_hp > 0 else 0
        if hp_percent > 0.6:
            hp_color = COLOR_HEALTH_HIGH
        elif hp_percent > 0.3:
            hp_color = COLOR_HEALTH_MED
        else:
            hp_color = COLOR_HEALTH_LOW
        
        hp_bar = self._make_bar(self.player_hp, self.player_max_hp, 20)
        
        # Energy bar
        en_bar = self._make_bar(self.player_energy, self.player_max_energy, 20)
        
        # Skills
        skills_text = ""
        for skill in self.skills[:4]:  # Show first 4 skills
            name = skill.get("name", "?")
            key = skill.get("key", "?")
            cd = skill.get("cooldown", 0)
            cd_str = f"CD:{cd}" if cd > 0 else "READY"
            skills_text += f"{key}: {name:12} {cd_str}\n"
        
        # Wave info
        wave_info = f"Wave {self.wave} | Enemies: {self.enemies_remaining}"
        
        content = (
            f"[{hp_color}]HP: {hp_bar} {self.player_hp}/{self.player_max_hp}[/]\n"
            f"[{COLOR_ENERGY}]EN: {en_bar} {self.player_energy}/{self.player_max_energy}[/]\n\n"
            f"{skills_text}"
            f"\n{wave_info}"
        )
        
        return Panel(content, title="Status", border_style="bold white")

    def _make_bar(self, current: int, maximum: int, length: int) -> str:
        """Create a visual progress bar."""
        if maximum <= 0:
            return "·" * length
        
        filled = int((current / maximum) * length)
        empty = length - filled
        
        return "█" * filled + "░" * empty


class CombatLog(Static):
    """Combat log widget."""

    messages = reactive([])

    def __init__(self, *args, max_lines: int = 8, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_lines = max_lines
        self.messages = []

    def add_message(self, message: str, style: str = "") -> None:
        """Add a message to the combat log."""
        self.messages.append((message, style))
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)
        self.refresh()

    def render(self) -> Panel:
        """Render the combat log."""
        content = ""
        for msg, style in self.messages:
            if style:
                content += f"[{style}]{msg}[/]\n"
            else:
                content += f"{msg}\n"
        
        if not content:
            content = "[dim]Combat log empty...[/]"
        
        return Panel(content, title="Combat Log", border_style="dim")


class GameScreen(Screen):
    """Main game screen."""

    CSS = """
    Screen {
        background: $surface;
    }
    
    #game-container {
        layout: horizontal;
        height: 100%;
    }
    
    #arena-panel {
        width: 70%;
        height: 100%;
    }
    
    #ui-panel {
        width: 30%;
        height: 100%;
        layout: vertical;
    }
    
    #hud {
        height: auto;
    }
    
    #combat-log {
        height: 1fr;
    }
    """

    BINDINGS = [
        ("up", "move_up", "Up"),
        ("down", "move_down", "Down"),
        ("left", "move_left", "Left"),
        ("right", "move_right", "Right"),
        ("q", "skill_q", "Skill Q"),
        ("w", "skill_w", "Skill W"),
        ("e", "skill_e", "Skill E"),
        ("r", "skill_r", "Skill R"),
        ("space", "wait", "Wait"),
        ("escape", "pause", "Pause"),
    ]

    def __init__(self, game_state: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state or {}
        self.arena_map = {}
        self.entities = []
        self.combat_messages = []

    def compose(self):
        """Compose the game screen."""
        with Container(id="game-container"):
            with Container(id="arena-panel"):
                yield ArenaDisplay(id="arena-display")
            
            with Container(id="ui-panel"):
                yield HUD(id="hud")
                yield CombatLog(id="combat-log")

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        self.set_interval(0.1, self._update_display)

    def _update_display(self) -> None:
        """Periodically update the display."""
        arena_display = self.query_one("#arena-display", ArenaDisplay)
        hud = self.query_one("#hud", HUD)
        
        if arena_display:
            arena_display.arena_map = self.arena_map
            arena_display.entities = self.entities
            arena_display.refresh()
        
        if hud:
            # Update HUD from game state
            player = self.game_state.get("player", {})
            hud.player_hp = player.get("hp", 100)
            hud.player_max_hp = player.get("max_hp", 100)
            hud.player_energy = player.get("energy", 50)
            hud.player_max_energy = player.get("max_energy", 50)
            hud.skills = player.get("skills", [])
            hud.wave = self.game_state.get("wave", 1)
            hud.enemies_remaining = self.game_state.get("enemies_remaining", 0)
            hud.refresh()

    def action_move_up(self) -> None:
        self._handle_input("up")

    def action_move_down(self) -> None:
        self._handle_input("down")

    def action_move_left(self) -> None:
        self._handle_input("left")

    def action_move_right(self) -> None:
        self._handle_input("right")

    def action_skill_q(self) -> None:
        self._handle_input("skill_q")

    def action_skill_w(self) -> None:
        self._handle_input("skill_w")

    def action_skill_e(self) -> None:
        self._handle_input("skill_e")

    def action_skill_r(self) -> None:
        self._handle_input("skill_r")

    def action_wait(self) -> None:
        self._handle_input("wait")

    def action_pause(self) -> None:
        self._handle_input("pause")

    def _handle_input(self, action: str) -> None:
        """Handle player input."""
        # Input will be processed by the game engine
        if "callback" in self.game_state:
            self.game_state["callback"](action)

    def log_combat(self, message: str, style: str = "") -> None:
        """Add a message to the combat log."""
        combat_log = self.query_one("#combat-log", CombatLog)
        if combat_log:
            combat_log.add_message(message, style)

    def set_arena(self, arena_map: dict) -> None:
        """Set the arena map."""
        self.arena_map = arena_map

    def set_entities(self, entities: list) -> None:
        """Set the entity list."""
        self.entities = entities
