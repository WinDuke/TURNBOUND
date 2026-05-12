"""Title screen with animated ASCII art and character selection."""

from textual.app import Screen
from textual.widgets import Static, Label
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from rich.text import Text
import random


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
            })

    def render(self) -> Text:
        """Render the animated background."""
        text = Text()
        
        grid = [[" " for _ in range(80)] for _ in range(24)]
        
        for particle in self.particles:
            x = int(particle["x"]) % 80
            y = int(particle["y"]) % 24
            if 0 <= y < 24 and 0 <= x < 80:
                grid[y][x] = particle["char"]
        
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
        logo_lines = [
            " ████████╗██╗  ██╗███████╗   ███████╗██╗  ██╗███████╗",
            " ╚══██╔══╝██║  ██║██╔════╝   ██╔════╝╚██╗██╔╝██╔════╝",
            "    ██║   ███████║█████╗     ███████╗ ╚███╔╝ ███████╗",
            "    ██║   ██╔══██║██╔══╝     ╚════██║ ██╔██╗ ╚════██║",
            "    ██║   ██║  ██║███████╗██╗███████║██╔╝ ██╗███████║",
            "    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝",
        ]
        
        text = Text()
        glow_colors = ["#ff00ff", "#ff44ff", "#ff88ff", "#ff44ff"]
        base_color = glow_colors[int(self.glow_intensity) % len(glow_colors)]
        
        for line in logo_lines:
            text.append(line + "\n", style=f"bold {base_color}")
        
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

    def __init__(self, label: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label

    def render(self) -> Text:
        """Render the menu button."""
        text = Text()
        
        if self.highlighted:
            text.append(f"  ► {self.label} ◄  ", style="bold #00ff00")
        else:
            text.append(f"    {self.label}    ", style="#888888")
        
        return text


class CharacterOption(Static):
    """Character selection option widget."""

    selected = reactive(False)

    def __init__(self, char_data: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_data = char_data

    def render(self) -> Text:
        """Render the character option."""
        text = Text()
        prefix = "► " if self.selected else "  "
        color = self.char_data.get("color", "#ffffff")
        name = self.char_data.get("name", "Unknown")
        symbol = self.char_data.get("symbol", "?")
        
        if self.selected:
            text.append(f"{prefix}[bold {color}]{symbol} {name}[/]")
        else:
            text.append(f"{prefix}[{color}]{symbol} {name}[/]")
        
        return text


class CharacterSelectScreen(Screen):
    """Character selection screen."""

    CSS = """
    Screen {
        background: #0a0a1a;
    }
    
    #char-container {
        layout: vertical;
        align: center middle;
        width: 100%;
        height: 100%;
    }
    
    #title {
        height: auto;
        content-align: center top;
        margin-bottom: 2;
    }
    
    #characters {
        height: auto;
        margin-top: 2;
    }
    
    .char-option {
        height: 3;
        width: 60;
        margin: 1;
        padding: 1;
    }
    
    .char-option.selected {
        background: #1a1a2e;
    }
    
    #char-description {
        height: auto;
        margin-top: 2;
        padding: 1;
    }
    
    #input-hints {
        dock: bottom;
        height: 3;
        padding: 1;
    }
    """

    BINDINGS = [
        ("up", "char_up", "Navigate Up"),
        ("down", "char_down", "Navigate Down"),
        ("enter", "select", "Select"),
        ("escape", "back", "Back"),
    ]

    CHARACTERS = [
        {
            "id": "executioner",
            "name": "THE EXECUTIONER",
            "desc": "Brutal blood-fueled melee fighter. Rage increases power at low HP.",
            "color": "#ff4444",
            "symbol": "⚔",
        },
        {
            "id": "astromancer",
            "name": "THE ASTROMANCER",
            "desc": "Temporal manipulation. Skills create echoes that repeat after turns.",
            "color": "#8844ff",
            "symbol": "✦",
        },
        {
            "id": "plague_saint",
            "name": "THE PLAGUE SAINT",
            "desc": "Infection master. Spreads plague and explodes infected enemies.",
            "color": "#44ff44",
            "symbol": "☠",
        },
        {
            "id": "mirror_duelist",
            "name": "THE MIRROR DUELIST",
            "desc": "Precision fighter. Counters attacks and guarantees critical hits.",
            "color": "#44ffff",
            "symbol": "◊",
        },
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_index = 0

    def compose(self):
        """Compose the character select screen."""
        with Container(id="char-container"):
            title = Text("SELECT YOUR CHAMPION", style="bold #ff00ff")
            yield Static(title, id="title")
            
            with Vertical(id="characters"):
                for i, char in enumerate(self.CHARACTERS):
                    widget = CharacterOption(char, classes="char-option")
                    widget.char_id = char["id"]
                    widget.char_index = i
                    if i == 0:
                        widget.selected = True
                        widget.add_class("selected")
                    yield widget
            
            desc_text = Text(self.CHARACTERS[0]["desc"], style=self.CHARACTERS[0]["color"])
            yield Static(desc_text, id="char-description")
        
        hints = Text()
        hints.append("↑↓ Select Character\n", style="#666666")
        hints.append("ENTER Confirm\n", style="#666666")
        hints.append("ESC Back", style="#666666")
        yield Static(hints, id="input-hints")

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        self._update_selection()

    def _update_selection(self) -> None:
        """Update which character is highlighted."""
        widgets = list(self.query(".char-option"))
        for i, widget in enumerate(widgets):
            if i == self.char_index:
                widget.selected = True
                widget.add_class("selected")
            else:
                widget.selected = False
                widget.remove_class("selected")
        
        # Update description
        char = self.CHARACTERS[self.char_index]
        desc_widget = self.query_one("#char-description", Static)
        desc_text = Text(char["desc"], style=char["color"])
        desc_widget.update(desc_text)

    def action_char_up(self) -> None:
        """Move selection up."""
        self.char_index = (self.char_index - 1) % len(self.CHARACTERS)
        self._update_selection()

    def action_char_down(self) -> None:
        """Move selection down."""
        self.char_index = (self.char_index + 1) % len(self.CHARACTERS)
        self._update_selection()

    def action_select(self) -> None:
        """Handle character selection."""
        selected_char = self.CHARACTERS[self.char_index]
        self.app.start_new_game(selected_char)

    def action_back(self) -> None:
        """Go back to title screen."""
        self.app.pop_screen()


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
                    yield MenuButton(option, classes="menu-item")
        
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
            self.app.push_screen("character_select")
        elif selected == "CHARACTERS":
            self.app.push_screen("character_select")
        elif selected == "EXIT GAME" or selected == "QUIT":
            self.app.exit()
        else:
            pass

    def action_quit(self) -> None:
        """Quit the game."""
        self.app.exit()
