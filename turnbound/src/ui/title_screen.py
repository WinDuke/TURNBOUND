"""Title screen with animated ASCII art."""

from textual.app import Screen
from textual.widgets import Static, Label, Button
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
import random
import asyncio


class AnimatedBackground(Static):
    """Animated background with drifting particles."""

    frame = reactive(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particles = []
        self._init_particles()

    def _init_particles(self) -> None:
        """Initialize floating particles."""
        self.particles = []
        for _ in range(30):
            self.particles.append({
                "x": random.randint(0, 79),
                "y": random.randint(0, 23),
                "speed": random.uniform(0.1, 0.5),
                "char": random.choice(["·", "░", "✦", "*"]),
                "color": random.choice(["#444444", "#666666", "#888888"]),
            })

    def render(self) -> Text:
        """Render the animated background."""
        text = Text()
        
        # Create empty grid
        grid = [[" " for _ in range(80)] for _ in range(24)]
        
        # Place particles
        for particle in self.particles:
            x = int(particle["x"]) % 80
            y = int(particle["y"]) % 24
            if 0 <= y < 24 and 0 <= x < 80:
                grid[y][x] = particle["char"]
        
        # Render grid
        for row in grid:
            for char in row:
                if char != " ":
                    text.append(char, style="#444466")
                else:
                    text.append(" ")
            text.append("\n")
        
        return text

    def on_mount(self) -> None:
        """Start animation loop."""
        self.set_interval(0.1, self._animate)

    def _animate(self) -> None:
        """Update particle positions."""
        for particle in self.particles:
            particle["y"] += particle["speed"]
            if particle["y"] >= 24:
                particle["y"] = 0
                particle["x"] = random.randint(0, 79)
        
        self.frame += 1
        self.refresh()


class TitleLogo(Static):
    """Animated title logo."""

    glow_intensity = reactive(0)

    def render(self) -> Text:
        """Render the title logo."""
        # ASCII art logo
        logo_lines = [
            " ████████╗██╗  ██╗███████╗   ███████╗██╗  ██╗███████╗",
            " ╚══██╔══╝██║  ██║██╔════╝   ██╔════╝╚██╗██╔╝██╔════╝",
            "    ██║   ███████║█████╗     ███████╗ ╚███╔╝ ███████╗",
            "    ██║   ██╔══██║██╔══╝     ╚════██║ ██╔██╗ ╚════██║",
            "    ██║   ██║  ██║███████╗██╗███████║██╔╝ ██╗███████║",
            "    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝",
        ]
        
        text = Text()
        
        # Glow colors cycling
        glow_colors = ["#ff00ff", "#ff44ff", "#ff88ff", "#ff44ff"]
        base_color = glow_colors[int(self.glow_intensity) % len(glow_colors)]
        
        for line in logo_lines:
            text.append(line + "\n", style=f"bold {base_color}")
        
        # Subtitle
        text.append("\n", style="dim")
        text.append("   A Turn-Based Survival Roguelike", style="italic #888888")
        
        return text

    def on_mount(self) -> None:
        """Start glow animation."""
        self.set_interval(0.2, self._pulse_glow)

    def _pulse_glow(self) -> None:
        """Pulse the glow effect."""
        self.glow_intensity = (self.glow_intensity + 1) % 4
        self.refresh()


class MenuButton(Static):
    """Styled menu button."""

    highlighted = reactive(False)

    def __init__(self, label: str, action: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self.action = action

    def render(self) -> Text:
        """Render the menu button."""
        text = Text()
        
        if self.highlighted:
            text.append(f"  ► {self.label} ◄  ", style="bold #00ff00")
        else:
            text.append(f"    {self.label}    ", style="#888888")
        
        return text


class TitleScreen(Screen):
    """Main title screen."""

    CSS = """
    Screen {
        background: #0a0a1a;
    }
    
    #title-container {
        layout: vertical;
        align: center middle;
        width: 100%;
        height: 100%;
    }
    
    #logo {
        height: auto;
        content-align: center top;
    }
    
    #menu {
        height: auto;
        margin-top: 3;
    }
    
    .menu-item {
        height: 1;
        content-align: center middle;
    }
    
    #input-hints {
        dock: bottom;
        height: 3;
        padding: 1;
    }
    """

    BINDINGS = [
        ("up", "menu_up", "Navigate Up"),
        ("down", "menu_down", "Navigate Down"),
        ("enter", "select", "Select"),
        ("q", "quit", "Quit"),
    ]

    menu_index = reactive(0)

    MENU_OPTIONS = [
        "START GAME",
        "CHARACTERS",
        "BESTIARY",
        "SETTINGS",
        "CREDITS",
        "EXIT GAME",
    ]

    def compose(self):
        """Compose the title screen."""
        yield AnimatedBackground(id="background")
        
        with Container(id="title-container"):
            yield TitleLogo(id="logo")
            
            with Vertical(id="menu"):
                for option in self.MENU_OPTIONS:
                    yield MenuButton(option, option.lower(), classes="menu-item")
        
        # Input hints at bottom
        hints = Text()
        hints.append("↑↓ Navigate\n", style="#666666")
        hints.append("ENTER Select\n", style="#666666")
        hints.append("Q Quit", style="#666666")
        yield Static(hints, id="input-hints")

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        self._update_menu_highlight()

    def _update_menu_highlight(self) -> None:
        """Update which menu item is highlighted."""
        buttons = list(self.query(".menu-item"))
        for i, button in enumerate(buttons):
            if hasattr(button, "highlighted"):
                button.highlighted = (i == self.menu_index)

    def action_menu_up(self) -> None:
        """Move menu selection up."""
        self.menu_index = (self.menu_index - 1) % len(self.MENU_OPTIONS)
        self._update_menu_highlight()

    def action_menu_down(self) -> None:
        """Move menu selection down."""
        self.menu_index = (self.menu_index + 1) % len(self.MENU_OPTIONS)
        self._update_menu_highlight()

    def action_select(self) -> None:
        """Handle menu selection."""
        selected = self.MENU_OPTIONS[self.menu_index]
        
        if selected == "START GAME":
            self.app.push_screen("game")
        elif selected == "EXIT GAME" or selected == "QUIT":
            self.app.exit()
        else:
            # Placeholder for other menus
            pass

    def action_quit(self) -> None:
        """Quit the game."""
        self.app.exit()
