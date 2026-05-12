"""
TURNBOUND - Core Constants
"""

# Screen & Arena Dimensions
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
ARENA_WIDTH = 50
ARENA_HEIGHT = 25

# Tile Symbols
TILE_EMPTY = "."
TILE_WALL = "#"
TILE_FLOOR = "·"
TILE_OBSTACLE = "▓"

# Game States
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_BOSS = "BOSS"
STATE_GAMEOVER = "GAMEOVER"
STATE_PAUSED = "PAUSED"
STATE_LEVELUP = "LEVELUP"

# Damage Types
DAMAGE_TYPES = [
    "physical",
    "fire",
    "frost",
    "lightning",
    "void",
    "poison",
    "blood"
]

# Status Effects
STATUS_EFFECTS = [
    "burn",
    "poison",
    "shock",
    "freeze",
    "bleed",
    "vulnerable",
    "weakness"
]

# Factions
FACTION_PLAYER = "player"
FACTION_ENEMY = "enemy"
FACTION_NEUTRAL = "neutral"

# Render Layers
LAYER_TERRAIN = 0
LAYER_OBJECTS = 1
LAYER_UNITS = 2
LAYER_EFFECTS = 3
LAYER_PARTICLES = 4
LAYER_UI = 5

# Input Keys
KEY_MOVE_UP = "up"
KEY_MOVE_DOWN = "down"
KEY_MOVE_LEFT = "left"
KEY_MOVE_RIGHT = "right"
KEY_SKILL_Q = "q"
KEY_SKILL_W = "w"
KEY_SKILL_E = "e"
KEY_SKILL_R = "r"
KEY_WAIT = "space"
KEY_PAUSE = "escape"
KEY_INSPECT = "tab"
