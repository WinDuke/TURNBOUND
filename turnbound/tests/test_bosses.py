"""Tests for boss system."""

import pytest
from src.content.bosses import (
    get_boss,
    get_all_bosses,
    create_boss_entity_data,
    get_boss_phase,
    check_boss_phase_transition,
)


class TestBosses:
    """Test boss definitions and encounter system."""

    def test_get_all_bosses(self):
        """Should return 3 bosses."""
        bosses = get_all_bosses()
        assert len(bosses) == 3
        
        boss_ids = {b["id"] for b in bosses}
        assert "hollow_king" in boss_ids
        assert "bell_saint" in boss_ids
        assert "choir_of_teeth" in boss_ids

    def test_get_boss_by_id(self):
        """Should return specific boss by ID."""
        boss = get_boss("hollow_king")
        assert boss is not None
        assert boss["name"] == "The Hollow King"
        assert len(boss["phases"]) == 3

    def test_create_boss_entity_data(self):
        """Should create valid entity data for boss."""
        data = create_boss_entity_data("bell_saint", 25, 10)
        
        assert data["position"]["x"] == 25
        assert data["position"]["y"] == 10
        assert data["health"]["current"] == 280  # Bell Saint base HP
        assert data["faction"]["alignment"] == "boss"
        assert "boss" in data
        assert data["boss"]["phase"] == 1

    def test_unknown_boss_raises_error(self):
        """Should raise error for unknown boss."""
        with pytest.raises(ValueError):
            create_boss_entity_data("unknown_boss", 0, 0)

    def test_get_boss_phase(self):
        """Should return correct phase data."""
        boss = get_boss("hollow_king")
        
        phase_1 = get_boss_phase(boss, 1)
        assert phase_1["id"] == "phase_1"
        assert phase_1["name"] == "Duelist"
        
        phase_2 = get_boss_phase(boss, 2)
        assert phase_2["id"] == "phase_2"
        assert phase_2["name"] == "Mirror Clones"

    def test_check_boss_phase_transition(self):
        """Should detect phase transitions based on health."""
        boss = get_boss("hollow_king")
        
        # Full health - stay in phase 1
        new_phase = check_boss_phase_transition(300, 300, 1, boss)
        assert new_phase == 1
        
        # 60% health - should transition to phase 2 (threshold is 0.66)
        new_phase = check_boss_phase_transition(180, 300, 1, boss)
        assert new_phase == 2
        
        # 25% health from phase 2 - should transition to phase 3 (threshold is 0.33)
        new_phase = check_boss_phase_transition(75, 300, 2, boss)
        assert new_phase == 3

    def test_bell_saint_bell_mechanic(self):
        """Bell Saint should have bell ring mechanic."""
        boss = get_boss("bell_saint")
        
        assert "bell_rings_every" in boss
        assert boss["bell_rings_every"] == 4
        assert len(boss["bell_effects"]) == 4

    def test_choir_of_teeth_environment_boss(self):
        """Choir of Teeth should be an environment boss."""
        boss = get_boss("choir_of_teeth")
        
        assert boss.get("is_environment") is True
        assert "arena_mechanics" in boss
        assert boss["arena_mechanics"]["moving_walls"] is True

    def test_boss_tags(self):
        """All bosses should have appropriate tags."""
        for boss in get_all_bosses():
            assert "BOSS" in boss.get("tags", [])
        
        hollow_king = get_boss("hollow_king")
        assert "UNDEAD" in hollow_king["tags"]
        assert "ROYAL" in hollow_king["tags"]

    def test_boss_renderable_symbols(self):
        """Bosses should have unique renderable symbols."""
        for boss in get_all_bosses():
            renderable = boss.get("renderable", {})
            assert "symbol" in renderable
            assert "color" in renderable
            assert renderable.get("bold") is True
