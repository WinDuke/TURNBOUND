"""Tests for combat system."""

import pytest
from src.ecs.entity_manager import EntityManager
from src.core.event_bus import EventBus
from src.components import Health, Stats, Statuses, Faction, Position, Renderable
from src.systems.combat_system import CombatSystem


@pytest.fixture
def combat_setup():
    """Set up combat testing environment."""
    em = EntityManager()
    event_bus = EventBus()
    combat = CombatSystem(em, event_bus)
    
    # Create attacker
    attacker_id = em.create_entity()
    em.add_component(attacker_id, "stats", Stats(power=10, crit_chance=0.5, crit_multiplier=2.0))
    
    # Create defender
    defender_id = em.create_entity()
    em.add_component(defender_id, "health", Health(current=100, max=100))
    em.add_component(defender_id, "stats", Stats(defense=5))
    
    return {
        "em": em,
        "event_bus": event_bus,
        "combat": combat,
        "attacker_id": attacker_id,
        "defender_id": defender_id,
    }


def test_basic_damage(combat_setup):
    """Test basic damage calculation without crit."""
    result = combat_setup["combat"].calculate_damage(
        combat_setup["attacker_id"],
        combat_setup["defender_id"],
        base_damage=20,
        is_crit=False,
    )
    
    # Damage = (20 + 10) - 5 = 25
    assert result["damage"] == 25
    assert result["is_crit"] == False


def test_critical_hit(combat_setup):
    """Test critical hit damage calculation."""
    result = combat_setup["combat"].calculate_damage(
        combat_setup["attacker_id"],
        combat_setup["defender_id"],
        base_damage=20,
        is_crit=True,
    )
    
    # Damage = ((20 + 10) * 2.0) - 5 = 55
    assert result["damage"] == 55
    assert result["is_crit"] == True


def test_damage_application(combat_setup):
    """Test applying damage to health."""
    health = combat_setup["em"].get_component(combat_setup["defender_id"], "health")
    
    initial_hp = health.current
    actual_damage = combat_setup["combat"].apply_damage(
        combat_setup["defender_id"],
        damage=30,
    )
    
    assert actual_damage == 30
    assert health.current == initial_hp - 30


def test_damage_cannot_exceed_health(combat_setup):
    """Test that damage cannot reduce HP below 0."""
    health = combat_setup["em"].get_component(combat_setup["defender_id"], "health")
    health.current = 10
    
    actual_damage = combat_setup["combat"].apply_damage(
        combat_setup["defender_id"],
        damage=50,
    )
    
    assert actual_damage == 10  # Only 10 HP left
    assert health.current == 0


def test_healing(combat_setup):
    """Test healing an entity."""
    health = combat_setup["em"].get_component(combat_setup["defender_id"], "health")
    health.current = 50
    
    actual_heal = combat_setup["combat"].heal(
        combat_setup["defender_id"],
        amount=30,
    )
    
    assert actual_heal == 30
    assert health.current == 80


def test_healing_cannot_exceed_max(combat_setup):
    """Test that healing cannot exceed max HP."""
    health = combat_setup["em"].get_component(combat_setup["defender_id"], "health")
    health.current = 90
    
    actual_heal = combat_setup["combat"].heal(
        combat_setup["defender_id"],
        amount=50,
    )
    
    assert actual_heal == 10  # Only 10 HP to max
    assert health.current == 100


def test_status_application(combat_setup):
    """Test applying status effects."""
    statuses = Statuses()
    combat_setup["em"].add_component(combat_setup["defender_id"], "statuses", statuses)
    
    result = combat_setup["combat"].apply_status(
        combat_setup["defender_id"],
        status_id="burn",
        duration=3,
        stacks=1,
    )
    
    assert result == True
    assert statuses.has("burn")
    
    burn_data = statuses.get("burn")
    assert burn_data["duration"] == 3
    assert burn_data["stacks"] == 1


def test_status_stacking(combat_setup):
    """Test status effect stacking."""
    statuses = Statuses()
    combat_setup["em"].add_component(combat_setup["defender_id"], "statuses", statuses)
    
    combat_setup["combat"].apply_status(
        combat_setup["defender_id"],
        status_id="poison",
        duration=2,
        stacks=1,
    )
    
    combat_setup["combat"].apply_status(
        combat_setup["defender_id"],
        status_id="poison",
        duration=3,
        stacks=2,
    )
    
    poison_data = statuses.get("poison")
    assert poison_data["duration"] == 3  # Max duration
    assert poison_data["stacks"] == 3  # Stacks added


def test_minimum_damage(combat_setup):
    """Test that damage has a minimum of 1."""
    # Set defense very high
    defender_stats = combat_setup["em"].get_component(combat_setup["defender_id"], "stats")
    defender_stats.defense = 100
    
    result = combat_setup["combat"].calculate_damage(
        combat_setup["attacker_id"],
        combat_setup["defender_id"],
        base_damage=5,
        is_crit=False,
    )
    
    # Despite high defense, minimum damage is 1
    assert result["damage"] >= 1
