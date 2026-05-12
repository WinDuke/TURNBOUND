"""Character definitions and factory."""

from typing import Any


# Character skill definitions
EXECUTIONER_SKILLS = [
    {
        "id": "cleave",
        "name": "Cleave",
        "key": "Q",
        "range": 2,
        "radius": 1,
        "damage": 12,
        "damage_type": "physical",
        "cost": 10,
        "cooldown": 2,
        "tags": ["MELEE", "AOE"],
        "description": "Wide melee attack hitting all adjacent enemies",
    },
    {
        "id": "chain_hook",
        "name": "Chain Hook",
        "key": "W",
        "range": 5,
        "damage": 5,
        "damage_type": "physical",
        "cost": 15,
        "cooldown": 3,
        "tags": ["RANGED", "PULL"],
        "description": "Pull enemy to you and deal damage",
    },
    {
        "id": "blood_surge",
        "name": "Blood Surge",
        "key": "E",
        "range": 1,
        "damage": 20,
        "damage_type": "blood",
        "cost": 0,
        "health_cost": 15,
        "cooldown": 4,
        "tags": ["BLOOD", "SELF_DAMAGE"],
        "description": "Spend HP to deal massive damage",
    },
    {
        "id": "execution",
        "name": "Execution",
        "key": "R",
        "range": 2,
        "damage": 999,
        "damage_type": "physical",
        "cost": 25,
        "cooldown": 6,
        "tags": ["EXECUTE"],
        "execute_threshold": 0.3,
        "description": "Instantly kill enemy below 30% HP",
    },
]

ASTROMANCER_SKILLS = [
    {
        "id": "star_bolt",
        "name": "Star Bolt",
        "key": "Q",
        "range": 8,
        "damage": 10,
        "damage_type": "void",
        "cost": 12,
        "cooldown": 2,
        "tags": ["PROJECTILE", "PIERCE"],
        "description": "Piercing projectile that hits multiple enemies",
    },
    {
        "id": "warp_step",
        "name": "Warp Step",
        "key": "W",
        "range": 6,
        "damage": 0,
        "damage_type": "void",
        "cost": 20,
        "cooldown": 3,
        "tags": ["TELEPORT", "MOBILITY"],
        "description": "Teleport to target location",
    },
    {
        "id": "echo_seal",
        "name": "Echo Seal",
        "key": "E",
        "range": 0,
        "damage": 0,
        "cost": 15,
        "cooldown": 4,
        "tags": ["ECHO", "UTILITY"],
        "description": "Mark previous skill to repeat after 2 turns",
    },
    {
        "id": "collapse",
        "name": "Collapse",
        "key": "R",
        "range": 0,
        "damage": 15,
        "damage_type": "void",
        "cost": 30,
        "cooldown": 5,
        "tags": ["ECHO", "AOE"],
        "description": "Trigger all echo effects simultaneously",
    },
]

PLAGUE_SAINT_SKILLS = [
    {
        "id": "rot_touch",
        "name": "Rot Touch",
        "key": "Q",
        "range": 1,
        "damage": 8,
        "damage_type": "poison",
        "cost": 8,
        "cooldown": 1,
        "tags": ["MELEE", "POISON"],
        "apply_status": {"status": "poison", "duration": 4, "stacks": 2},
        "description": "Poisonous touch that applies poison stacks",
    },
    {
        "id": "spore_cloud",
        "name": "Spore Cloud",
        "key": "W",
        "range": 5,
        "radius": 2,
        "damage": 5,
        "damage_type": "poison",
        "cost": 18,
        "cooldown": 4,
        "tags": ["AOE", "POISON", "ZONE"],
        "apply_status": {"status": "poison", "duration": 3, "stacks": 1},
        "description": "Create infection field that poisons enemies",
    },
    {
        "id": "harvest",
        "name": "Harvest",
        "key": "E",
        "range": 6,
        "damage": 0,
        "cost": 15,
        "cooldown": 3,
        "tags": ["EXPLOSION", "POISON"],
        "description": "Explode infected enemies, spreading infection",
    },
    {
        "id": "bloom",
        "name": "Bloom",
        "key": "R",
        "range": 0,
        "radius": 5,
        "damage": 20,
        "damage_type": "poison",
        "cost": 35,
        "cooldown": 6,
        "tags": ["AOE", "POISON", "MASSIVE"],
        "apply_status": {"status": "poison", "duration": 5, "stacks": 3},
        "description": "Mass mutation causing explosions across arena",
    },
]

MIRROR_DUELIST_SKILLS = [
    {
        "id": "feint",
        "name": "Feint",
        "key": "Q",
        "range": 1,
        "damage": 5,
        "damage_type": "physical",
        "cost": 10,
        "cooldown": 2,
        "tags": ["MELEE", "SETUP"],
        "guaranteed_crit_next": True,
        "description": "Setup guaranteed critical strike on next attack",
    },
    {
        "id": "mirror_step",
        "name": "Mirror Step",
        "key": "W",
        "range": 4,
        "damage": 0,
        "cost": 15,
        "cooldown": 3,
        "tags": ["DASH", "ILLUSION"],
        "description": "Dash leaving behind an illusion",
    },
    {
        "id": "riposte",
        "name": "Riposte",
        "key": "E",
        "range": 0,
        "damage": 0,
        "cost": 20,
        "cooldown": 4,
        "tags": ["COUNTER", "STANCE"],
        "counter_stance": True,
        "description": "Enter counter stance, retaliate on enemy attacks",
    },
    {
        "id": "perfect_reflection",
        "name": "Perfect Reflection",
        "key": "R",
        "range": 0,
        "damage": 0,
        "cost": 30,
        "cooldown": 5,
        "tags": ["REFLECT", "UTILITY"],
        "reflect_next_skill": True,
        "description": "Reflect the next enemy skill back at them",
    },
]


CHARACTER_DEFINITIONS = {
    "executioner": {
        "id": "executioner",
        "name": "The Executioner",
        "description": "Brutal blood-fueled melee fighter. Lower HP increases power.",
        "theme": "blood",
        "mechanic": "rage",
        "base_stats": {
            "power": 15,
            "defense": 3,
            "crit_chance": 0.1,
            "crit_multiplier": 2.2,
            "speed": 0,
            "evasion": 0.0,
        },
        "base_health": 120,
        "base_energy": 40,
        "energy_regen": 4,
        "skills": EXECUTIONER_SKILLS,
        "passive_tags": ["BLOOD", "MELEE", "BERSERKER"],
        "renderable": {
            "symbol": "⚔",
            "color": "#ff3333",
            "bold": True,
        },
    },
    "astromancer": {
        "id": "astromancer",
        "name": "The Astromancer",
        "description": "Temporal and spatial manipulation. Abilities can repeat as echoes.",
        "theme": "void",
        "mechanic": "echo",
        "base_stats": {
            "power": 12,
            "defense": 1,
            "crit_chance": 0.08,
            "crit_multiplier": 2.5,
            "speed": 2,
            "evasion": 0.1,
        },
        "base_health": 80,
        "base_energy": 60,
        "energy_regen": 6,
        "skills": ASTROMANCER_SKILLS,
        "passive_tags": ["VOID", "ECHO", "RANGED"],
        "renderable": {
            "symbol": "✦",
            "color": "#9933ff",
            "bold": True,
            "blink": False,
        },
    },
    "plague_saint": {
        "id": "plague_saint",
        "name": "The Plague Saint",
        "description": "Infection and arena corruption. Spreads disease through enemies.",
        "theme": "poison",
        "mechanic": "infection",
        "base_stats": {
            "power": 10,
            "defense": 2,
            "crit_chance": 0.05,
            "crit_multiplier": 2.0,
            "speed": 0,
            "evasion": 0.05,
        },
        "base_health": 90,
        "base_energy": 50,
        "energy_regen": 5,
        "skills": PLAGUE_SAINT_SKILLS,
        "passive_tags": ["POISON", "AOE", "DOT"],
        "renderable": {
            "symbol": "☠",
            "color": "#33ff33",
            "bold": True,
        },
    },
    "mirror_duelist": {
        "id": "mirror_duelist",
        "name": "The Mirror Duelist",
        "description": "Precision, counters, prediction. Focus system for perfect timing.",
        "theme": "precision",
        "mechanic": "focus",
        "base_stats": {
            "power": 11,
            "defense": 2,
            "crit_chance": 0.15,
            "crit_multiplier": 2.8,
            "speed": 3,
            "evasion": 0.15,
        },
        "base_health": 85,
        "base_energy": 55,
        "energy_regen": 5,
        "skills": MIRROR_DUELIST_SKILLS,
        "passive_tags": ["PHYSICAL", "COUNTER", "CRIT"],
        "renderable": {
            "symbol": "◊",
            "color": "#33ccff",
            "bold": True,
        },
    },
}


def get_character(char_id: str) -> dict | None:
    """Get character definition by ID."""
    return CHARACTER_DEFINITIONS.get(char_id)


def get_all_characters() -> list[dict]:
    """Get all character definitions."""
    return list(CHARACTER_DEFINITIONS.values())


def create_character_entity_data(char_id: str, spawn_x: int, spawn_y: int) -> dict:
    """Create entity component data for a character."""
    char = get_character(char_id)
    if not char:
        raise ValueError(f"Unknown character: {char_id}")
    
    return {
        "position": {"x": spawn_x, "y": spawn_y},
        "renderable": char["renderable"],
        "health": {
            "current": char["base_health"],
            "max": char["base_health"],
        },
        "energy": {
            "current": char["base_energy"],
            "max": char["base_energy"],
            "regen": char["energy_regen"],
        },
        "stats": char["base_stats"],
        "skills": {
            "active": char["skills"],
            "passive": [],
            "triggered": [],
        },
        "cooldowns": {},
        "faction": {"alignment": "player"},
        "level": {"exp": 0, "level": 1, "exp_to_next": 100},
        "tags": {"tags": set(char["passive_tags"])},
        "statuses": {},
    }
