"""Content loading and management."""

from src.content.characters import (
    get_character,
    get_all_characters,
    create_character_entity_data,
    CHARACTER_DEFINITIONS,
)
from src.content.enemies import (
    get_enemy,
    get_all_enemies,
    get_elite_modifier,
    create_enemy_entity_data,
    get_enemy_cost,
    ENEMY_DEFINITIONS,
    ELITE_MODIFIERS,
)
from src.content.upgrades import (
    get_upgrades_by_rarity,
    get_all_upgrades,
    get_upgrade_by_id,
    generate_upgrade_choices,
    check_tag_synergies,
    apply_upgrade_effects,
    UPGRADE_POOL,
)
from src.content.bosses import (
    get_boss,
    get_all_bosses,
    create_boss_entity_data,
    get_boss_phase,
    check_boss_phase_transition,
    BOSS_DEFINITIONS,
)


__all__ = [
    # Characters
    "get_character",
    "get_all_characters",
    "create_character_entity_data",
    "CHARACTER_DEFINITIONS",
    # Enemies
    "get_enemy",
    "get_all_enemies",
    "get_elite_modifier",
    "create_enemy_entity_data",
    "get_enemy_cost",
    "ENEMY_DEFINITIONS",
    "ELITE_MODIFIERS",
    # Upgrades
    "get_upgrades_by_rarity",
    "get_all_upgrades",
    "get_upgrade_by_id",
    "generate_upgrade_choices",
    "check_tag_synergies",
    "apply_upgrade_effects",
    "UPGRADE_POOL",
    # Bosses
    "get_boss",
    "get_all_bosses",
    "create_boss_entity_data",
    "get_boss_phase",
    "check_boss_phase_transition",
    "BOSS_DEFINITIONS",
]