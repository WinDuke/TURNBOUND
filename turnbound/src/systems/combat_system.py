"""Combat system for damage, crits, and status interactions."""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ecs.entity_manager import EntityManager
    from src.core.event_bus import EventBus


class CombatSystem:
    """Handles all combat calculations and resolution."""

    def __init__(self, entity_manager: "EntityManager", event_bus: "EventBus"):
        self.em = entity_manager
        self.event_bus = event_bus

    def calculate_damage(
        self,
        attacker_id: int,
        defender_id: int,
        base_damage: int,
        damage_type: str = "physical",
        is_crit: bool | None = None,
    ) -> dict:
        """
        Calculate final damage between two entities.
        
        Returns dict with:
        - damage: final damage amount
        - is_crit: whether it was a critical hit
        - modifiers: list of applied modifiers
        """
        attacker_stats = self.em.get_component(attacker_id, "stats")
        defender_stats = self.em.get_component(defender_id, "stats")
        defender_health = self.em.get_component(defender_id, "health")
        defender_statuses = self.em.get_component(defender_id, "statuses")
        
        if not attacker_stats or not defender_health:
            return {"damage": 0, "is_crit": False, "modifiers": []}
        
        modifiers = []
        
        # Base damage calculation
        damage = base_damage + attacker_stats.power
        
        # Critical hit check
        if is_crit is None:
            crit_chance = attacker_stats.crit_chance
            # Check for guaranteed crit from statuses
            if defender_statuses and defender_statuses.has("vulnerable"):
                crit_chance += 0.25
                modifiers.append("vulnerable_crit_bonus")
            
            is_crit = random.random() < crit_chance
        
        if is_crit:
            damage *= attacker_stats.crit_multiplier
            modifiers.append("critical_hit")
        
        # Apply defense
        if defender_stats:
            defense = defender_stats.defense
            
            # Check for defense reduction from statuses
            if defender_statuses:
                if defender_statuses.has("weakness"):
                    weakness = defender_statuses.get("weakness")
                    defense = int(defense * 0.5)
                    modifiers.append("weakness_defense_reduction")
            
            damage = max(1, damage - defense)
        
        # Status interactions
        if defender_statuses:
            # Shock increases damage taken
            if defender_statuses.has("shock"):
                shock_data = defender_statuses.get("shock")
                shock_bonus = shock_data.get("bonus", 0.5)
                damage = int(damage * (1 + shock_bonus))
                modifiers.append("shock_damage_bonus")
                
                # Remove shock after triggering
                defender_statuses.remove("shock")
                self.event_bus.emit("status_remove", {
                    "entity_id": defender_id,
                    "status": "shock"
                })
            
            # Freeze takes extra damage from heavy hits
            if defender_statuses.has("freeze") and base_damage >= 15:
                shatter_bonus = 0.5
                damage = int(damage * (1 + shatter_bonus))
                modifiers.append("freeze_shatter")
                defender_statuses.remove("freeze")
                self.event_bus.emit("status_remove", {
                    "entity_id": defender_id,
                    "status": "freeze"
                })
        
        # Ensure minimum damage
        damage = max(1, damage)
        
        return {
            "damage": damage,
            "is_crit": is_crit,
            "modifiers": modifiers,
        }

    def apply_damage(
        self,
        target_id: int,
        damage: int,
        damage_type: str = "physical",
        source_id: int | None = None,
    ) -> int:
        """Apply damage to an entity and return actual damage dealt."""
        health = self.em.get_component(target_id, "health")
        if not health:
            return 0
        
        actual_damage = health.damage(damage)
        
        # Emit events
        self.event_bus.emit("damage_dealt", {
            "target_id": target_id,
            "source_id": source_id,
            "damage": actual_damage,
            "damage_type": damage_type,
        })
        
        # Check for death
        if not health.is_alive():
            self.event_bus.emit("kill", {
                "victim_id": target_id,
                "killer_id": source_id,
            })
        
        return actual_damage

    def apply_status(
        self,
        target_id: int,
        status_id: str,
        duration: int,
        stacks: int = 1,
        data: dict | None = None,
    ) -> bool:
        """Apply a status effect to an entity."""
        statuses = self.em.get_component(target_id, "statuses")
        if not statuses:
            # Add statuses component if missing
            from src.components import Statuses
            statuses = Statuses()
            self.em.add_component(target_id, "statuses", statuses)
        
        # Check for immunity
        if statuses.has(status_id):
            existing = statuses.get(status_id)
            if existing.get("data", {}).get("immune", False):
                return False
        
        statuses.add(status_id, duration, stacks, data)
        
        self.event_bus.emit("status_apply", {
            "entity_id": target_id,
            "status": status_id,
            "duration": duration,
            "stacks": stacks,
        })
        
        return True

    def tick_statuses(self, entity_id: int) -> list[dict]:
        """Tick status effects and return triggered effects."""
        statuses = self.em.get_component(entity_id, "statuses")
        if not statuses:
            return []
        
        effects = []
        expired = statuses.tick()
        
        for status_id in expired:
            effects.append({
                "type": "expired",
                "status": status_id,
            })
            self.event_bus.emit("status_remove", {
                "entity_id": entity_id,
                "status": status_id,
            })
        
        # Apply ongoing effects
        for status_id, status_data in statuses.effects.items():
            effect = self._apply_status_effect(entity_id, status_id, status_data)
            if effect:
                effects.append(effect)
        
        return effects

    def _apply_status_effect(
        self,
        entity_id: int,
        status_id: str,
        status_data: dict,
    ) -> dict | None:
        """Apply the ongoing effect of a status."""
        health = self.em.get_component(entity_id, "health")
        if not health:
            return None
        
        stacks = status_data.get("stacks", 1)
        effect = None
        
        if status_id == "burn":
            damage = 3 * stacks
            actual = health.damage(damage)
            effect = {
                "type": "damage_over_time",
                "status": status_id,
                "damage": actual,
            }
        
        elif status_id == "poison":
            damage = 2 * stacks
            actual = health.damage(damage)
            effect = {
                "type": "damage_over_time",
                "status": status_id,
                "damage": actual,
            }
        
        elif status_id == "bleed":
            # Bleed triggers on movement (handled by movement system)
            pass
        
        return effect

    def heal(self, target_id: int, amount: int, source_id: int | None = None) -> int:
        """Heal an entity and return actual healing done."""
        health = self.em.get_component(target_id, "health")
        if not health:
            return 0
        
        actual_heal = health.heal(amount)
        
        self.event_bus.emit("heal", {
            "target_id": target_id,
            "source_id": source_id,
            "amount": actual_heal,
        })
        
        return actual_heal
