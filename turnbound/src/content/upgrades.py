"""Upgrade definitions and generation system."""

import random
from typing import Any


# Upgrade pool organized by rarity and tags
UPGRADE_POOL = {
    # Common upgrades - simple modifiers
    "common": [
        {
            "id": "sharp_edges",
            "name": "Sharp Edges",
            "rarity": "common",
            "description": "+10% physical damage",
            "tags": ["PHYSICAL"],
            "effects": {"damage_bonus_physical": 0.1},
        },
        {
            "id": "hardened_skin",
            "name": "Hardened Skin",
            "rarity": "common",
            "description": "+2 Defense",
            "tags": ["DEFENSE"],
            "effects": {"defense_flat": 2},
        },
        {
            "id": "vitality",
            "name": "Vitality",
            "rarity": "common",
            "description": "+15 Max HP",
            "tags": ["HEALTH"],
            "effects": {"health_max": 15},
        },
        {
            "id": "energy_drink",
            "name": "Energy Drink",
            "rarity": "common",
            "description": "+10 Max Energy, +1 Energy Regen",
            "tags": ["ENERGY"],
            "effects": {"energy_max": 10, "energy_regen": 1},
        },
        {
            "id": "keen_eye",
            "name": "Keen Eye",
            "rarity": "common",
            "description": "+3% Crit Chance",
            "tags": ["CRIT"],
            "effects": {"crit_chance": 0.03},
        },
        {
            "id": "burning_touch",
            "name": "Burning Touch",
            "rarity": "common",
            "description": "Attacks have 15% chance to apply Burn",
            "tags": ["FIRE", "ATTACK"],
            "effects": {"on_hit_apply": {"status": "burn", "duration": 2, "chance": 0.15}},
        },
        {
            "id": "poison_coating",
            "name": "Poison Coating",
            "rarity": "common",
            "description": "Attacks have 15% chance to apply Poison",
            "tags": ["POISON", "ATTACK"],
            "effects": {"on_hit_apply": {"status": "poison", "duration": 2, "chance": 0.15}},
        },
        {
            "id": "shock_charge",
            "name": "Shock Charge",
            "rarity": "common",
            "description": "Attacks have 15% chance to apply Shock",
            "tags": ["LIGHTNING", "ATTACK"],
            "effects": {"on_hit_apply": {"status": "shock", "duration": 2, "chance": 0.15}},
        },
        
        # Dash/movement upgrades
        {
            "id": "swift_steps",
            "name": "Swift Steps",
            "rarity": "common",
            "description": "+1 Movement range",
            "tags": ["DASH", "MOBILITY"],
            "effects": {"movement_range": 1},
        },
        {
            "id": "evasion_training",
            "name": "Evasion Training",
            "rarity": "common",
            "description": "+5% Evasion",
            "tags": ["MOBILITY", "DEFENSE"],
            "effects": {"evasion": 0.05},
        },
    ],
    
    # Rare upgrades - mechanic changers
    "rare": [
        {
            "id": "ignition_dashes",
            "name": "Ignition Dashes",
            "rarity": "rare",
            "description": "Dash ignites tiles, burning enemies who cross them",
            "tags": ["FIRE", "DASH"],
            "effects": {
                "dash_leaves_fire": True,
                "fire_duration": 3,
            },
        },
        {
            "id": "blood_for_power",
            "name": "Blood for Power",
            "rarity": "rare",
            "description": "Losing 10% HP grants +20% damage for 2 turns",
            "tags": ["BLOOD", "BERSERKER"],
            "effects": {
                "low_hp_damage_bonus": {"threshold": 0.1, "bonus": 0.2, "duration": 2},
            },
        },
        {
            "id": "echo_master",
            "name": "Echo Master",
            "rarity": "rare",
            "description": "Echo skills repeat one additional time",
            "tags": ["ECHO", "VOID"],
            "effects": {
                "echo_extra_repeat": 1,
            },
        },
        {
            "id": "infection_spread",
            "name": "Infection Spread",
            "rarity": "rare",
            "description": "Killing poisoned enemy spreads poison to nearby foes",
            "tags": ["POISON", "AOE"],
            "effects": {
                "poison_explosion_on_kill": {"radius": 2, "duration": 3},
            },
        },
        {
            "id": "counter_master",
            "name": "Counter Master",
            "rarity": "rare",
            "description": "Successful counters refund 50% energy cost",
            "tags": ["COUNTER", "ENERGY"],
            "effects": {
                "counter_energy_refund": 0.5,
            },
        },
        {
            "id": "glass_cannon",
            "name": "Glass Cannon",
            "rarity": "rare",
            "description": "+30% damage, -20% max HP",
            "tags": ["BERSERKER", "RISK"],
            "effects": {
                "damage_bonus_all": 0.3,
                "health_max_mult": 0.8,
            },
        },
        {
            "id": "tank_buster",
            "name": "Tank Buster",
            "rarity": "rare",
            "description": "Deal +50% damage to enemies with Defense > 5",
            "tags": ["PHYSICAL", "ANTI_TANK"],
            "effects": {
                "high_armor_damage_bonus": {"armor_threshold": 5, "bonus": 0.5},
            },
        },
        {
            "id": "frostbite",
            "name": "Frostbite",
            "rarity": "rare",
            "description": "Freeze lasts 1 turn longer, frozen enemies take +40% damage",
            "tags": ["FROST", "CONTROL"],
            "effects": {
                "freeze_duration_bonus": 1,
                "freeze_damage_bonus": 0.4,
            },
        },
    ],
    
    # Epic upgrades - build defining
    "epic": [
        {
            "id": "chain_lightning",
            "name": "Chain Lightning",
            "rarity": "epic",
            "description": "Lightning damage chains to 2 additional targets",
            "tags": ["LIGHTNING", "AOE"],
            "effects": {
                "lightning_chain_count": 2,
            },
        },
        {
            "id": "executioner_instinct",
            "name": "Executioner Instinct",
            "rarity": "epic",
            "description": "Execute threshold increased to 50%, execute restores 20 HP",
            "tags": ["EXECUTE", "BLOOD"],
            "effects": {
                "execute_threshold": 0.5,
                "execute_heal": 20,
            },
        },
        {
            "id": "temporal_loop",
            "name": "Temporal Loop",
            "rarity": "epic",
            "description": "Once per combat, revive with 50% HP on death",
            "tags": ["VOID", "ECHO", "SURVIVAL"],
            "effects": {
                "once_per_combat_revive": {"hp_percent": 0.5},
            },
        },
        {
            "id": "plague_carrier",
            "name": "Plague Carrier",
            "rarity": "epic",
            "description": "You constantly emit poison clouds, immune to poison",
            "tags": ["POISON", "AOE", "IMMUNITY"],
            "effects": {
                "passive_poison_aura": {"radius": 1, "duration": 2},
                "poison_immunity": True,
            },
        },
        {
            "id": "mirror_image",
            "name": "Mirror Image",
            "rarity": "epic",
            "description": "Create illusion every 3 turns that distracts enemies",
            "tags": ["ILLUSION", "UTILITY"],
            "effects": {
                "illusion_spawn_interval": 3,
            },
        },
        {
            "id": "unstoppable_force",
            "name": "Unstoppable Force",
            "rarity": "epic",
            "description": "Movement attacks deal double damage and cannot miss",
            "tags": ["DASH", "PHYSICAL", "ATTACK"],
            "effects": {
                "charge_attack_double_damage": True,
                "charge_attack_guaranteed_hit": True,
            },
        },
        {
            "id": "ritual_sacrifice",
            "name": "Ritual Sacrifice",
            "rarity": "epic",
            "description": "Killing an enemy instantly refreshes all cooldowns (once per 5 turns)",
            "tags": ["BLOOD", "COOLDOWN"],
            "effects": {
                "kill_reset_cooldowns": {"cooldown": 5},
            },
        },
    ],
    
    # Legendary upgrades - game breaking
    "legendary": [
        {
            "id": "phoenix_engine",
            "name": "Phoenix Engine",
            "rarity": "legendary",
            "description": "Burn explosions create firestorms that spread across the arena",
            "tags": ["FIRE", "AOE", "EXPLOSION"],
            "effects": {
                "burn_explosion_firestorm": True,
                "firestorm_spread": True,
            },
        },
        {
            "id": "echo_cascade",
            "name": "Echo Cascade",
            "rarity": "legendary",
            "description": "Repeated spells can repeat again, creating infinite loops (max 3 repeats)",
            "tags": ["ECHO", "VOID", "INFINITE"],
            "effects": {
                "echo_can_echo": True,
                "max_echo_depth": 3,
            },
        },
        {
            "id": "crimson_reactor",
            "name": "Crimson Reactor",
            "rarity": "legendary",
            "description": "Taking damage restores 15% of damage taken as Energy",
            "tags": ["BLOOD", "ENERGY", "RECOVERY"],
            "effects": {
                "damage_to_energy": 0.15,
            },
        },
        {
            "id": "glass_momentum",
            "name": "Glass Momentum",
            "rarity": "legendary",
            "description": "Every dodge increases Crit Damage by 50% for next attack (stacks to 500%)",
            "tags": ["CRIT", "EVASION", "SNOWBALL"],
            "effects": {
                "dodge_crit_damage_stack": 0.5,
                "max_crit_damage_stacks": 10,
            },
        },
        {
            "id": "void_walker",
            "name": "Void Walker",
            "rarity": "legendary",
            "description": "Teleporting through enemies deals massive void damage",
            "tags": ["VOID", "TELEPORT", "AOE"],
            "effects": {
                "teleport_collision_damage": 25,
                "teleport_collision_type": "void",
            },
        },
        {
            "id": "eternal_plague",
            "name": "Eternal Plague",
            "rarity": "legendary",
            "description": "Enemies killed by poison rise as zombie allies",
            "tags": ["POISON", "SUMMON", "UNDEAD"],
            "effects": {
                "poison_kill_raise_zombie": True,
            },
        },
        {
            "id": "perfect_form",
            "name": "Perfect Form",
            "rarity": "legendary",
            "description": "All attacks are guaranteed critical hits when at full HP",
            "tags": ["CRIT", "PERFECT"],
            "effects": {
                "full_hp_guaranteed_crit": True,
            },
        },
        {
            "id": "annihilation",
            "name": "Annihilation",
            "rarity": "legendary",
            "description": "Skills cost no energy but have double cooldown",
            "tags": ["ENERGY", "COOLDOWN", "HIGH_RISK"],
            "effects": {
                "skills_zero_cost": True,
                "cooldown_multiplier": 2.0,
            },
        },
    ],
}


# Tag synergies - unlock special upgrades based on tag combinations
TAG_SYNERGIES = {
    ("FIRE", "DASH"): {
        "unlock_upgrade": "ignition_dashes",
        "description": "Fire + Dash synergy unlocked",
    },
    ("FIRE", "AOE"): {
        "unlock_upgrade": "phoenix_engine",
        "description": "Fire + AOE synergy unlocked",
    },
    ("ECHO", "VOID"): {
        "unlock_upgrade": "echo_cascade",
        "description": "Echo + Void synergy unlocked",
    },
    ("BLOOD", "ENERGY"): {
        "unlock_upgrade": "crimson_reactor",
        "description": "Blood + Energy synergy unlocked",
    },
    ("POISON", "AOE"): {
        "unlock_upgrade": "infection_spread",
        "description": "Poison + AOE synergy unlocked",
    },
    ("CRIT", "EVASION"): {
        "unlock_upgrade": "glass_momentum",
        "description": "Crit + Evasion synergy unlocked",
    },
    ("EXECUTE", "BLOOD"): {
        "unlock_upgrade": "executioner_instinct",
        "description": "Execute + Blood synergy unlocked",
    },
}


def get_upgrades_by_rarity(rarity: str) -> list[dict]:
    """Get all upgrades of a specific rarity."""
    return UPGRADE_POOL.get(rarity, [])


def get_all_upgrades() -> list[dict]:
    """Get all upgrades from all rarities."""
    all_upgrades = []
    for rarity_pool in UPGRADE_POOL.values():
        all_upgrades.extend(rarity_pool)
    return all_upgrades


def get_upgrade_by_id(upgrade_id: str) -> dict | None:
    """Get upgrade definition by ID."""
    for rarity_pool in UPGRADE_POOL.values():
        for upgrade in rarity_pool:
            if upgrade["id"] == upgrade_id:
                return upgrade
    return None


def generate_upgrade_choices(
    player_tags: set[str],
    used_damage_types: set[str],
    num_choices: int = 3,
    min_rarity: str = "common",
) -> list[dict]:
    """
    Generate upgrade choices for level up.
    
    Considers player tags and damage types to provide synergistic options.
    """
    rarity_order = ["common", "rare", "epic", "legendary"]
    
    # Determine available rarities based on progression
    # For MVP, we'll use a simple system: more rare upgrades as you progress
    available_rarities = ["common"]
    
    # Add higher rarities based on some criteria (for now, random chance)
    if random.random() < 0.4:
        available_rarities.append("rare")
    if random.random() < 0.15:
        available_rarities.append("epic")
    if random.random() < 0.05:
        available_rarities.append("legendary")
    
    # Collect eligible upgrades
    eligible = []
    for rarity in available_rarities:
        if rarity_order.index(rarity) >= rarity_order.index(min_rarity):
            eligible.extend(UPGRADE_POOL.get(rarity, []))
    
    # Score upgrades by synergy with player build
    scored = []
    for upgrade in eligible:
        score = 1.0
        upgrade_tags = set(upgrade.get("tags", []))
        
        # Bonus for matching player tags
        matching_tags = player_tags & upgrade_tags
        score += len(matching_tags) * 0.5
        
        # Bonus for matching damage types
        if any(tag in used_damage_types for tag in upgrade_tags):
            score += 0.3
        
        # Small random factor for variety
        score += random.uniform(0, 0.3)
        
        scored.append((score, upgrade))
    
    # Sort by score and pick top candidates
    scored.sort(reverse=True, key=lambda x: x[0])
    
    # Select num_choices with some randomness
    choices = []
    candidates = scored[:max(num_choices * 2, 6)]  # Consider top candidates
    
    while len(choices) < num_choices and candidates:
        # Weighted random selection
        total_score = sum(s for s, _ in candidates)
        if total_score <= 0:
            break
            
        roll = random.uniform(0, total_score)
        cumulative = 0
        selected_idx = 0
        
        for i, (score, _) in enumerate(candidates):
            cumulative += score
            if roll <= cumulative:
                selected_idx = i
                break
        
        _, chosen = candidates.pop(selected_idx)
        choices.append(chosen)
    
    return choices


def check_tag_synergies(player_tags: set[str]) -> list[dict]:
    """Check for unlocked tag synergies."""
    unlocked = []
    
    for tag_combo, synergy_data in TAG_SYNERGIES.items():
        if all(tag in player_tags for tag in tag_combo):
            unlocked.append({
                "combo": tag_combo,
                "upgrade_id": synergy_data["unlock_upgrade"],
                "description": synergy_data["description"],
            })
    
    return unlocked


def apply_upgrade_effects(entity_manager: Any, entity_id: int, upgrade: dict) -> None:
    """Apply upgrade effects to an entity."""
    effects = upgrade.get("effects", {})
    
    # Get or create necessary components
    stats = entity_manager.get_component(entity_id, "stats")
    health = entity_manager.get_component(entity_id, "health")
    energy = entity_manager.get_component(entity_id, "energy")
    tags = entity_manager.get_component(entity_id, "tags")
    
    # Apply stat modifications
    if stats:
        if "damage_bonus_physical" in effects:
            # Store as tag for combat system to reference
            tags.add("DAMAGE_BONUS_PHYSICAL")
        
        if "defense_flat" in effects:
            stats.defense += effects["defense_flat"]
        
        if "crit_chance" in effects:
            stats.crit_chance += effects["crit_chance"]
        
        if "evasion" in effects:
            stats.evasion += effects["evasion"]
    
    # Apply health modifications
    if health:
        if "health_max" in effects:
            health.max += effects["health_max"]
            health.current += effects["health_max"]
        
        if "health_max_mult" in effects:
            health.max = int(health.max * effects["health_max_mult"])
            health.current = min(health.current, health.max)
    
    # Apply energy modifications
    if energy:
        if "energy_max" in effects:
            energy.max += effects["energy_max"]
            energy.current += effects["energy_max"]
        
        if "energy_regen" in effects:
            energy.regen += effects["energy_regen"]
    
    # Add tags for conditional effects
    for effect_key, effect_value in effects.items():
        if effect_key.startswith("on_") or effect_key.endswith("_bonus"):
            tags.add(effect_key.upper())
    
    # Special effects stored in tags component data
    if hasattr(tags, 'data'):
        for effect_key, effect_value in effects.items():
            tags.data[effect_key] = effect_value
