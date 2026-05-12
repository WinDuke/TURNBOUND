"""Enemy definitions and factory."""

from typing import Any


# Basic enemy types
ENEMY_DEFINITIONS = {
    # Swarmers - cheap, numerous
    "zombie": {
        "id": "zombie",
        "name": "Zombie",
        "description": "Shambling corpse that overwhelms with numbers",
        "type": "swarmer",
        "cost": 2,
        "base_stats": {
            "power": 5,
            "defense": 0,
            "crit_chance": 0.0,
            "crit_multiplier": 1.5,
            "speed": -1,
            "evasion": 0.0,
        },
        "base_health": 25,
        "base_energy": 0,
        "skills": [],
        "tags": ["UNDEAD", "SWARMER"],
        "renderable": {
            "symbol": "z",
            "color": "#556b2f",
            "bold": False,
        },
        "ai_behavior": "aggressive",
    },
    "rat": {
        "id": "rat",
        "name": "Plague Rat",
        "description": "Diseased vermin that spreads infection",
        "type": "swarmer",
        "cost": 2,
        "base_stats": {
            "power": 3,
            "defense": 0,
            "crit_chance": 0.1,
            "crit_multiplier": 1.5,
            "speed": 2,
            "evasion": 0.2,
        },
        "base_health": 15,
        "base_energy": 0,
        "skills": [],
        "tags": ["BEAST", "SWARMER"],
        "apply_status_on_hit": {"status": "poison", "duration": 2, "chance": 0.3},
        "renderable": {
            "symbol": "r",
            "color": "#8b4513",
            "bold": False,
        },
        "ai_behavior": "aggressive",
    },
    "skeleton": {
        "id": "skeleton",
        "name": "Skeleton Warrior",
        "description": "Animated bones wielding rusty weapons",
        "type": "swarmer",
        "cost": 3,
        "base_stats": {
            "power": 6,
            "defense": 1,
            "crit_chance": 0.05,
            "crit_multiplier": 1.5,
            "speed": 0,
            "evasion": 0.0,
        },
        "base_health": 30,
        "base_energy": 0,
        "skills": [],
        "tags": ["UNDEAD", "SWARMER"],
        "renderable": {
            "symbol": "s",
            "color": "#cccccc",
            "bold": False,
        },
        "ai_behavior": "aggressive",
    },
    
    # Hunters - ranged, keep distance
    "spitter": {
        "id": "spitter",
        "name": "Acid Spitter",
        "description": "Mutated creature that spews corrosive bile",
        "type": "hunter",
        "cost": 4,
        "base_stats": {
            "power": 8,
            "defense": 0,
            "crit_chance": 0.1,
            "crit_multiplier": 1.8,
            "speed": 0,
            "evasion": 0.1,
        },
        "base_health": 35,
        "base_energy": 30,
        "skills": [
            {
                "id": "acid_spit",
                "name": "Acid Spit",
                "range": 5,
                "damage": 10,
                "damage_type": "poison",
                "cost": 10,
                "cooldown": 2,
                "apply_status": {"status": "poison", "duration": 3},
            }
        ],
        "tags": ["BEAST", "HUNTER", "RANGED"],
        "renderable": {
            "symbol": "S",
            "color": "#32cd32",
            "bold": True,
        },
        "ai_behavior": "defensive",
    },
    "archer": {
        "id": "archer",
        "name": "Bone Archer",
        "description": "Undead marksman with deadly aim",
        "type": "hunter",
        "cost": 5,
        "base_stats": {
            "power": 9,
            "defense": 0,
            "crit_chance": 0.15,
            "crit_multiplier": 2.0,
            "speed": 1,
            "evasion": 0.05,
        },
        "base_health": 30,
        "base_energy": 25,
        "skills": [
            {
                "id": "piercing_shot",
                "name": "Piercing Shot",
                "range": 6,
                "damage": 12,
                "damage_type": "physical",
                "cost": 8,
                "cooldown": 2,
            }
        ],
        "tags": ["UNDEAD", "HUNTER", "RANGED"],
        "renderable": {
            "symbol": "a",
            "color": "#daa520",
            "bold": False,
        },
        "ai_behavior": "defensive",
    },
    
    # Tanks - high HP, block movement
    "knight": {
        "id": "knight",
        "name": "Cursed Knight",
        "description": "Armored warrior bound by dark magic",
        "type": "tank",
        "cost": 6,
        "base_stats": {
            "power": 10,
            "defense": 4,
            "crit_chance": 0.05,
            "crit_multiplier": 1.5,
            "speed": -2,
            "evasion": 0.0,
        },
        "base_health": 60,
        "base_energy": 0,
        "skills": [],
        "tags": ["UNDEAD", "TANK", "ARMORED"],
        "renderable": {
            "symbol": "K",
            "color": "#708090",
            "bold": True,
        },
        "ai_behavior": "aggressive",
    },
    "golem": {
        "id": "golem",
        "name": "Stone Golem",
        "description": "Animated construct of stone and magic",
        "type": "tank",
        "cost": 8,
        "base_stats": {
            "power": 12,
            "defense": 6,
            "crit_chance": 0.0,
            "crit_multiplier": 1.5,
            "speed": -3,
            "evasion": 0.0,
        },
        "base_health": 80,
        "base_energy": 0,
        "skills": [],
        "tags": ["CONSTRUCT", "TANK", "ARMORED"],
        "renderable": {
            "symbol": "G",
            "color": "#8b8b8b",
            "bold": True,
        },
        "ai_behavior": "tactical",
    },
    
    # Casters - control zones, status effects
    "necromancer": {
        "id": "necromancer",
        "name": "Necromancer",
        "description": "Dark mage commanding the dead",
        "type": "caster",
        "cost": 10,
        "base_stats": {
            "power": 15,
            "defense": 1,
            "crit_chance": 0.1,
            "crit_multiplier": 2.0,
            "speed": 0,
            "evasion": 0.1,
        },
        "base_health": 40,
        "base_energy": 50,
        "skills": [
            {
                "id": "raise_dead",
                "name": "Raise Dead",
                "range": 4,
                "damage": 0,
                "cost": 20,
                "cooldown": 4,
                "spawn_minion": "zombie",
            },
            {
                "id": "dark_bolt",
                "name": "Dark Bolt",
                "range": 5,
                "damage": 14,
                "damage_type": "void",
                "cost": 12,
                "cooldown": 2,
            },
        ],
        "tags": ["UNDEAD", "CASTER", "SUMMONER"],
        "renderable": {
            "symbol": "N",
            "color": "#9932cc",
            "bold": True,
        },
        "ai_behavior": "defensive",
    },
    "cultist": {
        "id": "cultist",
        "name": "Blood Cultist",
        "description": "Fanatic devoted to dark powers",
        "type": "caster",
        "cost": 7,
        "base_stats": {
            "power": 12,
            "defense": 1,
            "crit_chance": 0.08,
            "crit_multiplier": 1.8,
            "speed": 0,
            "evasion": 0.05,
        },
        "base_health": 35,
        "base_energy": 40,
        "skills": [
            {
                "id": "blood_curse",
                "name": "Blood Curse",
                "range": 5,
                "damage": 8,
                "damage_type": "blood",
                "cost": 15,
                "cooldown": 3,
                "apply_status": {"status": "weakness", "duration": 3},
            },
            {
                "id": "burning_blood",
                "name": "Burning Blood",
                "range": 4,
                "damage": 10,
                "damage_type": "fire",
                "cost": 12,
                "cooldown": 3,
                "apply_status": {"status": "burn", "duration": 3},
            },
        ],
        "tags": ["HUMAN", "CASTER", "BLOOD"],
        "renderable": {
            "symbol": "C",
            "color": "#8b0000",
            "bold": True,
        },
        "ai_behavior": "tactical",
    },
    
    # Support - buff enemies
    "priest": {
        "id": "priest",
        "name": "Dark Priest",
        "description": "Corrupted healer spreading corruption",
        "type": "support",
        "cost": 8,
        "base_stats": {
            "power": 8,
            "defense": 2,
            "crit_chance": 0.05,
            "crit_multiplier": 1.5,
            "speed": 0,
            "evasion": 0.05,
        },
        "base_health": 45,
        "base_energy": 45,
        "skills": [
            {
                "id": "dark_blessing",
                "name": "Dark Blessing",
                "range": 4,
                "damage": 0,
                "cost": 15,
                "cooldown": 4,
                "buff_allies": {"power": 3, "duration": 4},
            },
            {
                "id": "shadow_mend",
                "name": "Shadow Mend",
                "range": 4,
                "heal": 15,
                "cost": 18,
                "cooldown": 3,
            },
        ],
        "tags": ["UNDEAD", "SUPPORT", "BUFFER"],
        "renderable": {
            "symbol": "P",
            "color": "#4b0082",
            "bold": True,
        },
        "ai_behavior": "defensive",
    },
    "shaman": {
        "id": "shaman",
        "name": "Frost Shaman",
        "description": "Ice wielder slowing enemies",
        "type": "support",
        "cost": 7,
        "base_stats": {
            "power": 10,
            "defense": 1,
            "crit_chance": 0.08,
            "crit_multiplier": 1.8,
            "speed": 0,
            "evasion": 0.05,
        },
        "base_health": 40,
        "base_energy": 40,
        "skills": [
            {
                "id": "frost_nova",
                "name": "Frost Nova",
                "range": 4,
                "radius": 2,
                "damage": 6,
                "damage_type": "frost",
                "cost": 15,
                "cooldown": 3,
                "apply_status": {"status": "freeze", "duration": 2},
            },
        ],
        "tags": ["HUMAN", "SUPPORT", "CONTROL"],
        "renderable": {
            "symbol": "H",
            "color": "#00ffff",
            "bold": True,
        },
        "ai_behavior": "tactical",
    },
}


# Elite modifiers
ELITE_MODIFIERS = {
    "aggressive": {
        "id": "aggressive",
        "name": "Aggressive",
        "description": "Prioritizes pressure and attacks",
        "stat_modifiers": {
            "power": 1.3,
            "defense": 0.8,
            "speed": 1,
        },
        "health_modifier": 1.2,
        "ai_weights": {"attack": 1.5, "retreat": 0.5},
        "render_suffix": "!",
        "color_tint": "#ff4444",
    },
    "tactical": {
        "id": "tactical",
        "name": "Tactical",
        "description": "Avoids dangerous zones, smart positioning",
        "stat_modifiers": {
            "power": 1.1,
            "defense": 1.2,
            "evasion": 0.1,
        },
        "health_modifier": 1.1,
        "ai_weights": {"attack": 1.0, "retreat": 1.3, "position": 1.5},
        "render_suffix": "*",
        "color_tint": "#44ff44",
    },
    "frenzied": {
        "id": "frenzied",
        "name": "Frenzied",
        "description": "Ignores defense, attacks wildly",
        "stat_modifiers": {
            "power": 1.5,
            "defense": 0.5,
            "crit_chance": 0.1,
        },
        "health_modifier": 1.0,
        "ai_weights": {"attack": 2.0, "retreat": 0.0},
        "render_suffix": "💀",
        "color_tint": "#ff00ff",
    },
    "coward": {
        "id": "coward",
        "name": "Coward",
        "description": "Retreats on low HP",
        "stat_modifiers": {
            "speed": 1.5,
            "evasion": 0.2,
        },
        "health_modifier": 0.9,
        "ai_weights": {"attack": 0.5, "retreat": 2.0},
        "retreat_threshold": 0.3,
        "render_suffix": "?",
        "color_tint": "#ffff44",
    },
}


def get_enemy(enemy_id: str) -> dict | None:
    """Get enemy definition by ID."""
    return ENEMY_DEFINITIONS.get(enemy_id)


def get_all_enemies() -> list[dict]:
    """Get all enemy definitions."""
    return list(ENEMY_DEFINITIONS.values())


def get_elite_modifier(modifier_id: str) -> dict | None:
    """Get elite modifier definition."""
    return ELITE_MODIFIERS.get(modifier_id)


def create_enemy_entity_data(
    enemy_id: str,
    spawn_x: int,
    spawn_y: int,
    elite_modifier: str | None = None,
    wave_scaling: float = 1.0,
) -> dict:
    """Create entity component data for an enemy."""
    enemy = get_enemy(enemy_id)
    if not enemy:
        raise ValueError(f"Unknown enemy: {enemy_id}")
    
    # Apply wave scaling
    scale_mult = 1.0 + (wave_scaling - 1.0) * 0.5
    
    # Base data
    health = int(enemy["base_health"] * scale_mult)
    power = int(enemy["base_stats"]["power"] * scale_mult)
    
    # Apply elite modifier
    render_symbol = enemy["renderable"]["symbol"]
    render_color = enemy["renderable"]["color"]
    
    if elite_modifier:
        mod = get_elite_modifier(elite_modifier)
        if mod:
            health = int(health * mod.get("health_modifier", 1.0))
            power = int(power * mod.get("stat_modifiers", {}).get("power", 1.0))
            
            # Modify render
            suffix = mod.get("render_suffix", "")
            render_symbol = f"{render_symbol}{suffix}"
            render_color = mod.get("color_tint", render_color)
    
    return {
        "position": {"x": spawn_x, "y": spawn_y},
        "renderable": {
            "symbol": render_symbol,
            "color": render_color,
            "bold": enemy["renderable"].get("bold", False),
        },
        "health": {
            "current": health,
            "max": health,
        },
        "energy": {
            "current": enemy.get("base_energy", 0),
            "max": enemy.get("base_energy", 0),
            "regen": 3,
        },
        "stats": {
            "power": power,
            "defense": int(enemy["base_stats"]["defense"] * scale_mult),
            "crit_chance": enemy["base_stats"]["crit_chance"],
            "crit_multiplier": enemy["base_stats"]["crit_multiplier"],
            "speed": enemy["base_stats"]["speed"],
            "evasion": enemy["base_stats"]["evasion"],
        },
        "skills": {
            "active": enemy.get("skills", []),
            "passive": [],
            "triggered": [],
        },
        "cooldowns": {},
        "faction": {"alignment": "enemy"},
        "tags": {"tags": set(enemy.get("tags", []))},
        "statuses": {},
        "ai": {
            "behavior_type": enemy.get("ai_behavior", "aggressive"),
            "target_id": None,
            "elite_modifier": elite_modifier,
        },
    }


def get_enemy_cost(enemy_id: str, elite_modifier: str | None = None) -> int:
    """Get the threat budget cost of an enemy."""
    enemy = get_enemy(enemy_id)
    if not enemy:
        return 0
    
    cost = enemy["cost"]
    
    if elite_modifier:
        cost = int(cost * 1.5)
    
    return cost
