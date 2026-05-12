"""Core game constants."""

# Screen dimensions
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
ARENA_WIDTH = 50
ARENA_HEIGHT = 20

# Colors
COLOR_PLAYER = "#00ff00"
COLOR_ENEMY = "#ff0000"
COLOR_BOSS = "#ff00ff"
COLOR_TERRAIN = "#888888"
COLOR_OBSTACLE = "#666666"
COLOR_HIGHLIGHT = "#ffff00"
COLOR_UI_TEXT = "#ffffff"
COLOR_UI_DIM = "#666666"
COLOR_HEALTH_HIGH = "#00ff00"
COLOR_HEALTH_MED = "#ffff00"
COLOR_HEALTH_LOW = "#ff0000"
COLOR_ENERGY = "#0088ff"

# Damage types
DAMAGE_PHYSICAL = "physical"
DAMAGE_FIRE = "fire"
DAMAGE_FROST = "frost"
DAMAGE_LIGHTNING = "lightning"
DAMAGE_VOID = "void"
DAMAGE_POISON = "poison"
DAMAGE_BLOOD = "blood"

# Status effects
STATUS_BURN = "burn"
STATUS_POISON = "poison"
STATUS_SHOCK = "shock"
STATUS_FREEZE = "freeze"
STATUS_BLEED = "bleed"
STATUS_VULNERABLE = "vulnerable"
STATUS_WEAKNESS = "weakness"

# Factions
FACTION_PLAYER = "player"
FACTION_ENEMY = "enemy"
FACTION_NEUTRAL = "neutral"

# Game states
STATE_TITLE = "title"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_LEVELUP = "levelup"
STATE_GAMEOVER = "gameover"
STATE_BOSS_INTRO = "boss_intro"

# Input keys
KEY_UP = "up"
KEY_DOWN = "down"
KEY_LEFT = "left"
KEY_RIGHT = "right"
KEY_WAIT = "space"
KEY_SKILL_Q = "q"
KEY_SKILL_W = "w"
KEY_SKILL_E = "e"
KEY_SKILL_R = "r"
KEY_PAUSE = "escape"
KEY_INSPECT = "tab"

# Animation timing (ms)
ANIM_MIN_DURATION = 80
ANIM_MAX_DURATION = 250
ANIM_PROJECTILE = 150
ANIM_EXPLOSION = 200
ANIM_IMPACT = 100

# Wave system
WAVE_BASE_BUDGET = 10
WAVE_SCALING = 1.5
BOSS_WAVE_INTERVAL = 5

# Enemy costs
COST_ZOMBIE = 2
COST_SPITTER = 4
COST_KNIGHT = 6
COST_NECROMANCER = 10
COST_ELITE = 15

# Rarity levels
RARITY_COMMON = "common"
RARITY_RARE = "rare"
RARITY_EPIC = "epic"
RARITY_LEGENDARY = "legendary"
