"""
Main entry point for TURNBOUND.
Initializes the Textual app and starts the game loop.
"""
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Label, Button, Static
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual import events

from src.core.game import GameEngine
from src.components.position import Position
from src.components.renderable import Renderable

# --- Title Screen ---
class TitleScreen(Screen):
    """Stylized main menu."""
    
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("⚔️ TURNBOUND ⚔️", classes="title"),
            Label("A Tactical ASCII Roguelike", classes="subtitle"),
            Label("", classes="spacer"),
            Button("START GAME", id="start", classes="menu-btn"),
            Button("CHARACTERS", id="chars", classes="menu-btn"),
            Button("EXIT", id="exit", classes="menu-btn"),
            Label("↑↓ Navigate | ENTER Select", classes="hints"),
            classes="menu-container"
        )
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            # Default to Executioner for now
            self.app.start_game("executioner")
        elif event.button.id == "exit":
            self.app.exit()

# --- Game Screen ---
class GameScreen(Screen):
    """Main gameplay screen with arena and HUD."""
    
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.input_buffer = []
        
    def compose(self) -> ComposeResult:
        yield Container(
            Static("", id="arena-view"),
            Horizontal(
                Label("HP: --/--", id="hud-hp"),
                Label("EN: --/--", id="hud-en"),
                Label("Wave: 1", id="hud-wave"),
                id="hud-stats"
            ),
            Vertical(
                Label("Skills:", classes="skill-header"),
                Label("Q: Fireball", id="skill-q"),
                Label("W: Dash", id="skill-w"),
                Label("E: --", id="skill-e"),
                Label("R: --", id="skill-r"),
                id="skills-panel"
            ),
            Static("", id="combat-log"),
            id="game-layout"
        )
        
    def on_mount(self):
        self.refresh_display()
        self.set_focus()
        
    def refresh_display(self):
        """Render the arena and update HUD."""
        if not self.engine.current_arena:
            return
            
        # 1. Build display grid from arena
        grid = self.engine.current_arena["grid"]
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0
        
        # Create a mutable copy for rendering entities
        display_grid = [list(row) for row in grid]
        
        # 2. Overlay entities
        entities = self.engine.entities.query_components(["Position", "Renderable"])
        for eid in entities:
            pos = self.engine.entities.get_component(eid, "Position")
            ren = self.engine.entities.get_component(eid, "Renderable")
            
            if pos and ren:
                if 0 <= pos.y < height and 0 <= pos.x < width:
                    # Format with Rich style
                    symbol = f"[{ren.color}]{ren.symbol}[/]"
                    display_grid[pos.y][pos.x] = symbol
                    
        # 3. Convert to string
        arena_str = "\n".join("".join(str(cell) for cell in row) for row in display_grid)
        
        # Update Arena View
        try:
            self.query_one("#arena-view", Static).update(arena_str)
        except Exception:
            pass # Widget might not be ready
            
        # 4. Update HUD
        if self.engine.player_id:
            hp = self.engine.entities.get_component(self.engine.player_id, "Health")
            en = self.engine.entities.get_component(self.engine.player_id, "Energy")
            
            if hp:
                try:
                    self.query_one("#hud-hp", Label).update(f"HP: {hp.current_hp}/{hp.max_hp}")
                except Exception: pass
            if en:
                try:
                    self.query_one("#hud-en", Label).update(f"EN: {en.current}/{en.max_energy}")
                except Exception: pass
                
        # Update Wave info
        try:
            wave_lbl = self.query_one("#hud-wave", Label)
            wave_lbl.update(f"Wave: {self.engine.wave_system.current_wave}")
        except Exception: pass
        
        # Update Skill Cooldowns
        if self.engine.player_id:
            skills_comp = self.engine.entities.get_component(self.engine.player_id, "Skills")
            if skills_comp:
                skill_map = {"q": "fireball", "w": "dash", "e": None, "r": None} # Simplified
                for key, sid in [("q", "fireball"), ("w", "dash")]:
                    cd = skills_comp.cooldowns.get(sid, 0)
                    try:
                        self.query_one(f"#skill-{key}", Label).update(f"{key.upper()}: {sid} (CD: {cd})")
                    except Exception: pass

    def on_key(self, event: events.Key) -> None:
        """Handle player input."""
        if self.engine.game_state != "PLAYING":
            return
            
        action_type = None
        action_data = {}
        
        # Movement
        if event.key == "up":
            action_type, action_data = "MOVE", {"dx": 0, "dy": -1}
        elif event.key == "down":
            action_type, action_data = "MOVE", {"dx": 0, "dy": 1}
        elif event.key == "left":
            action_type, action_data = "MOVE", {"dx": -1, "dy": 0}
        elif event.key == "right":
            action_type, action_data = "MOVE", {"dx": 1, "dy": 0}
            
        # Skills
        elif event.key == "q":
            action_type, action_data = "SKILL", {"skill_id": "fireball", "target": None}
        elif event.key == "w":
            action_type, action_data = "SKILL", {"skill_id": "dash", "target": None}
            
        # Wait
        elif event.key == "space":
            action_type, action_data = "WAIT", {}
            
        # Process action
        if action_type:
            # Resolve target for skills if needed
            if action_type == "SKILL" and action_data["target"] is None:
                # Default to player pos or nearest enemy (simplified: player pos)
                p_pos = self.engine.entities.get_component(self.engine.player_id, "Position")
                if p_pos:
                    action_data["target"] = (p_pos.x, p_pos.y)
                    
            self.engine.process_turn(action_type, action_data)
            self.refresh_display()

# --- Main App ---
class TurnboundApp(App):
    """Main Textual Application."""
    
    CSS = """
    Screen {
        background: $surface-darken-3;
        color: $text;
    }
    
    .title {
        text-align: center;
        text-style: bold;
        color: red;
        padding: 2;
        font-size: 200%;
    }
    
    .subtitle {
        text-align: center;
        color: gray;
        padding-bottom: 2;
    }
    
    .menu-container {
        align: center middle;
        width: 100%;
        height: 100%;
    }
    
    .menu-btn {
        width: 50%;
        margin: 1;
    }
    
    .hints {
        text-align: center;
        color: blue;
        padding-top: 2;
    }
    
    #game-layout {
        layout: grid;
        grid-size: 2;
        grid-columns: 4fr 1fr;
        height: 100%;
        padding: 1;
    }
    
    #arena-view {
        background: $surface-darken-2;
        border: solid red;
        padding: 1;
        row-span: 3;
        content-align: left top;
    }
    
    #hud-stats {
        height: 3;
        align: left middle;
        padding-left: 1;
    }
    
    #skills-panel {
        border: solid blue;
        padding: 1;
        margin-top: 1;
    }
    
    .skill-header {
        text-style: bold;
        color: yellow;
    }
    
    #combat-log {
        height: 5;
        border: solid gray;
        padding: 1;
        overflow-y: auto;
        margin-top: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.engine = GameEngine()
        
    def on_mount(self) -> None:
        self.push_screen(TitleScreen(self.engine))

    def start_game(self, character_id: str):
        """Initialize game and switch to game screen."""
        self.engine.init_game(character_id)
        self.push_screen(GameScreen(self.engine))

if __name__ == "__main__":
    app = TurnboundApp()
    app.run()
