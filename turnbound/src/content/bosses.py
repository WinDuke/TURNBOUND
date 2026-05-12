"""Boss definitions and encounter system."""

from typing import Any


BOSS_DEFINITIONS = {
    "hollow_king": {
        "id": "hollow_king",
        "name": "The Hollow King",
        "description": "A fallen monarch consumed by darkness",
        "base_health": 300,
        "base_energy": 80,
        "base_stats": {
            "power": 18,
            "defense": 5,
            "crit_chance": 0.12,
            "crit_multiplier": 2.2,
            "speed": 1,
            "evasion": 0.08,
        },
        "phases": [
            {
                "id": "phase_1",
                "name": "Duelist",
                "health_threshold": 1.0,
                "description": "Aggressive duelist with precise strikes",
                "abilities": [
                    {
                        "id": "royal_strike",
                        "name": "Royal Strike",
                        "damage": 15,
                        "damage_type": "physical",
                        "cooldown": 2,
                        "target": "nearest",
                    },
                    {
                        "id": "crown_cleave",
                        "name": "Crown Cleave",
                        "damage": 20,
                        "damage_type": "physical",
                        "cooldown": 4,
                        "radius": 2,
                        "target": "player",
                    },
                ],
                "ai_weights": {"attack": 1.5, "defensive": 0.8},
            },
            {
                "id": "phase_2",
                "name": "Mirror Clones",
                "health_threshold": 0.66,
                "description": "Creates mirror clones to confuse and attack",
                "abilities": [
                    {
                        "id": "summon_clone",
                        "name": "Summon Clone",
                        "damage": 0,
                        "cooldown": 5,
                        "spawn_minion": "hollow_clone",
                        "count": 2,
                    },
                    {
                        "id": "shadow_bolt",
                        "name": "Shadow Bolt",
                        "damage": 18,
                        "damage_type": "void",
                        "cooldown": 2,
                        "target": "random",
                    },
                ],
                "ai_weights": {"attack": 1.2, "defensive": 1.0, "summon": 1.5},
            },
            {
                "id": "phase_3",
                "name": "Darkness Arena",
                "health_threshold": 0.33,
                "description": "Envelops arena in darkness, creating safe zones",
                "abilities": [
                    {
                        "id": "darkness_fall",
                        "name": "Darkness Fall",
                        "damage": 0,
                        "cooldown": 6,
                        "arena_effect": "darkness",
                        "duration": 5,
                    },
                    {
                        "id": "void_eruption",
                        "name": "Void Eruption",
                        "damage": 25,
                        "damage_type": "void",
                        "cooldown": 3,
                        "radius": 3,
                        "target": "player",
                    },
                ],
                "ai_weights": {"attack": 1.0, "defensive": 1.2, "area_control": 2.0},
            },
        ],
        "renderable": {
            "symbol": "♔",
            "color": "#ff00ff",
            "bold": True,
            "blink": True,
        },
        "tags": ["BOSS", "UNDEAD", "ROYAL"],
    },
    "bell_saint": {
        "id": "bell_saint",
        "name": "The Bell Saint",
        "description": "A corrupted saint whose bell marks the passage to death",
        "base_health": 280,
        "base_energy": 100,
        "base_stats": {
            "power": 15,
            "defense": 3,
            "crit_chance": 0.1,
            "crit_multiplier": 2.0,
            "speed": 0,
            "evasion": 0.1,
        },
        "bell_rings_every": 4,  # Turns between bell rings
        "bell_effects": [
            {
                "ring": 1,
                "name": "Haste",
                "effect": "boss_attacks_twice",
                "duration": 2,
            },
            {
                "ring": 2,
                "name": "Curse Field",
                "effect": "apply_weakness_all",
                "duration": 3,
            },
            {
                "ring": 3,
                "name": "Silence",
                "effect": "disable_player_skills",
                "duration": 2,
            },
            {
                "ring": 4,
                "name": "Judgment",
                "effect": "massive_aoe_damage",
                "damage": 30,
            },
        ],
        "phases": [
            {
                "id": "phase_1",
                "name": "Sanctified",
                "health_threshold": 1.0,
                "abilities": [
                    {
                        "id": "holy_smite",
                        "name": "Holy Smite",
                        "damage": 14,
                        "damage_type": "physical",
                        "cooldown": 2,
                    },
                    {
                        "id": "bell_toll",
                        "name": "Bell Toll",
                        "damage": 10,
                        "damage_type": "void",
                        "cooldown": 4,
                        "radius": 3,
                    },
                ],
            },
            {
                "id": "phase_2",
                "name": "Corrupted",
                "health_threshold": 0.5,
                "abilities": [
                    {
                        "id": "corrupted_smite",
                        "name": "Corrupted Smite",
                        "damage": 20,
                        "damage_type": "void",
                        "cooldown": 2,
                    },
                    {
                        "id": "curse_bell",
                        "name": "Curse Bell",
                        "damage": 15,
                        "damage_type": "blood",
                        "cooldown": 3,
                        "apply_status": {"status": "weakness", "duration": 3},
                    },
                ],
            },
        ],
        "renderable": {
            "symbol": "🔔",
            "color": "#ffd700",
            "bold": True,
        },
        "tags": ["BOSS", "HUMAN", "HOLY"],
    },
    "choir_of_teeth": {
        "id": "choir_of_teeth",
        "name": "Choir of Teeth",
        "description": "The arena itself becomes a living nightmare",
        "base_health": 400,
        "base_energy": 0,
        "base_stats": {
            "power": 20,
            "defense": 8,
            "crit_chance": 0.15,
            "crit_multiplier": 2.5,
            "speed": -1,
            "evasion": 0.0,
        },
        "is_environment": True,  # Boss is the arena
        "arena_mechanics": {
            "moving_walls": True,
            "shifting_safe_zones": True,
            "environmental_hazards": True,
        },
        "phases": [
            {
                "id": "phase_1",
                "name": "Awakening",
                "health_threshold": 1.0,
                "abilities": [
                    {
                        "id": "wall_shift",
                        "name": "Wall Shift",
                        "damage": 0,
                        "cooldown": 3,
                        "effect": "move_walls",
                    },
                    {
                        "id": "ground_spike",
                        "name": "Ground Spike",
                        "damage": 18,
                        "damage_type": "physical",
                        "cooldown": 2,
                        "target": "random_empty_tile",
                    },
                ],
            },
            {
                "id": "phase_2",
                "name": "Devouring",
                "health_threshold": 0.6,
                "abilities": [
                    {
                        "id": "crushing_walls",
                        "name": "Crushing Walls",
                        "damage": 25,
                        "damage_type": "physical",
                        "cooldown": 4,
                        "effect": "walls_damage_all",
                    },
                    {
                        "id": "safe_zone_shrink",
                        "name": "Safe Zone Shrink",
                        "damage": 0,
                        "cooldown": 3,
                        "effect": "reduce_safe_zone",
                    },
                ],
            },
            {
                "id": "phase_3",
                "name": "Annihilation",
                "health_threshold": 0.3,
                "abilities": [
                    {
                        "id": "total_collapse",
                        "name": "Total Collapse",
                        "damage": 35,
                        "damage_type": "void",
                        "cooldown": 5,
                        "radius": 5,
                        "target": "center",
                    },
                    {
                        "id": "teeth_eruption",
                        "name": "Teeth Eruption",
                        "damage": 20,
                        "damage_type": "physical",
                        "cooldown": 2,
                        "effect": "spawn_teeth_traps",
                    },
                ],
            },
        ],
        "renderable": {
            "symbol": "☠",
            "color": "#8b0000",
            "bold": True,
            "blink": True,
        },
        "tags": ["BOSS", "ENVIRONMENT", "ABOMINATION"],
    },
}


def get_boss(boss_id: str) -> dict | None:
    """Get boss definition by ID."""
    return BOSS_DEFINITIONS.get(boss_id)


def get_all_bosses() -> list[dict]:
    """Get all boss definitions."""
    return list(BOSS_DEFINITIONS.values())


def create_boss_entity_data(boss_id: str, spawn_x: int, spawn_y: int) -> dict:
    """Create entity component data for a boss."""
    boss = get_boss(boss_id)
    if not boss:
        raise ValueError(f"Unknown boss: {boss_id}")
    
    return {
        "position": {"x": spawn_x, "y": spawn_y},
        "renderable": boss["renderable"],
        "health": {
            "current": boss["base_health"],
            "max": boss["base_health"],
        },
        "energy": {
            "current": boss["base_energy"],
            "max": boss["base_energy"],
            "regen": 5,
        },
        "stats": boss["base_stats"],
        "skills": {
            "active": [],  # Populated from current phase
            "passive": [],
            "triggered": [],
        },
        "cooldowns": {},
        "faction": {"alignment": "boss"},
        "tags": {"tags": set(boss.get("tags", []))},
        "statuses": {},
        "boss": {
            "phase": 1,
            "phases": boss.get("phases", []),
            "script_state": "",
            "arena_effect": None,
            "bell_ring_counter": 0 if boss_id == "bell_saint" else None,
        },
    }


def get_boss_phase(boss_data: dict, current_phase: int) -> dict:
    """Get the current phase data for a boss."""
    phases = boss_data.get("phases", [])
    if not phases:
        return {}
    
    # Clamp phase to valid range
    phase_idx = min(current_phase - 1, len(phases) - 1)
    return phases[phase_idx]


def check_boss_phase_transition(
    boss_health_current: int,
    boss_health_max: int,
    current_phase: int,
    boss_data: dict,
) -> int:
    """Check if boss should transition to a new phase."""
    phases = boss_data.get("phases", [])
    if not phases or current_phase >= len(phases):
        return current_phase
    
    health_percent = boss_health_current / boss_health_max if boss_health_max > 0 else 0
    
    # Check thresholds for next phases
    for i in range(current_phase, len(phases)):
        phase = phases[i]
        threshold = phase.get("health_threshold", 0)
        
        if health_percent <= threshold:
            return i + 1  # Phases are 1-indexed
    
    return current_phase
