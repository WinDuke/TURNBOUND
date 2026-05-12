"""Render symbols and palettes."""

# ASCII Symbols
SYMBOLS = {
    # Terrain
    "floor": ".",
    "floor_alt": "·",
    "wall": "#",
    "wall_alt": "█",
    "obstacle": "▓",
    "water": "~",
    "lava": "≈",
    "ice": "*",
    
    # Player
    "player": "@",
    "player_alt": "☺",
    
    # Enemies
    "zombie": "z",
    "skeleton": "s",
    "knight": "K",
    "spitter": "p",
    "necromancer": "N",
    "ghost": "g",
    "demon": "D",
    "elite": "E",
    
    # Bosses
    "boss_hollow_king": "♔",
    "boss_bell_saint": "☮",
    "boss_choir": "☠",
    
    # Effects
    "fire": "🔥",
    "fire_ascii": ["░", "▒", "▓", "█"],
    "explosion": "💥",
    "explosion_ascii": ["*", "+", "✦", "✹"],
    "lightning": "⚡",
    "lightning_ascii": ["~", "≋", "⚡"],
    "poison": "☠",
    "poison_cloud": "☁",
    "blood": "💧",
    "blood_ascii": ["'", ".", ",", ";"],
    "sparkle": "✦",
    "star": "★",
    "skull": "☠",
    "cross": "†",
    "arrow_right": "→",
    "arrow_left": "←",
    "arrow_up": "↑",
    "arrow_down": "↓",
}

# Color Palettes
PALETTES = {
    "default": {
        "player": "#00ff00",
        "enemy": "#ff4444",
        "boss": "#ff00ff",
        "terrain_floor": "#444444",
        "terrain_wall": "#666666",
        "obstacle": "#888888",
        "ui_text": "#ffffff",
        "ui_dim": "#555555",
        "health_high": "#00ff00",
        "health_med": "#ffff00",
        "health_low": "#ff0000",
        "energy": "#0088ff",
        "highlight": "#ffff00",
    },
    "cemetery": {
        "player": "#88ff88",
        "enemy": "#aa4444",
        "boss": "#ff88ff",
        "terrain_floor": "#3a3a3a",
        "terrain_wall": "#555555",
        "obstacle": "#777777",
        "fog": "#2a2a2a",
        "accent": "#9999ff",
    },
    "crimson_cathedral": {
        "player": "#ff8888",
        "enemy": "#ff4444",
        "boss": "#ff0000",
        "terrain_floor": "#4a1a1a",
        "terrain_wall": "#662222",
        "blood": "#cc0000",
        "accent": "#ffaa00",
    },
    "frozen_hollow": {
        "player": "#88ffff",
        "enemy": "#4488ff",
        "boss": "#0044ff",
        "terrain_floor": "#1a2a3a",
        "terrain_wall": "#2a4a6a",
        "ice": "#aaddff",
        "accent": "#ffffff",
    },
    "void_fracture": {
        "player": "#ff88ff",
        "enemy": "#aa44aa",
        "boss": "#ff00ff",
        "terrain_floor": "#1a0a2a",
        "terrain_wall": "#3a1a5a",
        "void": "#6600aa",
        "accent": "#ff00ff",
    },
}

# Damage type colors
DAMAGE_COLORS = {
    "physical": "#cccccc",
    "fire": "#ff4400",
    "frost": "#00aaff",
    "lightning": "#ffdd00",
    "void": "#aa00ff",
    "poison": "#00ff00",
    "blood": "#ff0000",
}

# Status effect colors
STATUS_COLORS = {
    "burn": "#ff4400",
    "poison": "#00ff00",
    "shock": "#ffdd00",
    "freeze": "#00aaff",
    "bleed": "#ff0000",
    "vulnerable": "#ff8800",
    "weakness": "#888888",
}

# UI Styles
UI_STYLES = {
    "title": "bold italic #ff00ff",
    "subtitle": "dim #888888",
    "header": "bold #ffffff",
    "button": "bold #00ff00",
    "button_disabled": "dim #444444",
    "warning": "bold #ff0000",
    "info": "#0088ff",
    "success": "bold #00ff00",
}


def get_symbol(name: str, alt: bool = False) -> str:
    """Get a symbol by name."""
    if name not in SYMBOLS:
        return "?"
    
    symbol = SYMBOLS[name]
    if isinstance(symbol, list):
        import random
        return random.choice(symbol)
    return symbol


def get_palette(name: str) -> dict:
    """Get a color palette by name."""
    return PALETTES.get(name, PALETTES["default"])
