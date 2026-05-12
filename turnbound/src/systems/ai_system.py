"""Utility AI system for enemy behavior."""

import random
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.ecs.entity_manager import EntityManager
    from src.core.event_bus import EventBus


@dataclass
class ActionScore:
    """Scored action for utility AI."""
    action: str
    score: float
    target_id: Optional[int] = None
    data: dict = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}


class AISystem:
    """Utility AI system for enemy decision making."""

    def __init__(self, entity_manager: "EntityManager", event_bus: "EventBus"):
        self.em = entity_manager
        self.event_bus = event_bus
        
        # Base utility weights by behavior type
        self.base_weights = {
            "aggressive": {
                "attack": 1.0,
                "move_to_target": 0.8,
                "use_skill": 0.9,
                "retreat": 0.2,
            },
            "defensive": {
                "attack": 0.6,
                "move_to_target": 0.5,
                "use_skill": 0.7,
                "retreat": 0.8,
            },
            "tactical": {
                "attack": 0.7,
                "move_to_target": 0.6,
                "use_skill": 1.0,
                "retreat": 0.5,
            },
            "frenzied": {
                "attack": 1.2,
                "move_to_target": 1.0,
                "use_skill": 0.5,
                "retreat": 0.0,
            },
            "coward": {
                "attack": 0.3,
                "move_to_target": 0.2,
                "use_skill": 0.4,
                "retreat": 1.5,
            },
        }

    def decide_action(self, entity_id: int, player_id: Optional[int] = None) -> ActionScore:
        """
        Decide the best action for an entity using utility AI.
        
        Returns the highest scored action.
        """
        ai = self.em.get_component(entity_id, "ai")
        health = self.em.get_component(entity_id, "health")
        skills = self.em.get_component(entity_id, "skills")
        position = self.em.get_component(entity_id, "position")
        
        if not ai or not health or not position:
            return ActionScore("wait", 0.5)
        
        # Get behavior weights
        behavior = ai.behavior_type
        weights = self.base_weights.get(behavior, self.base_weights["aggressive"]).copy()
        
        # Apply elite modifier adjustments
        if ai.elite_modifier:
            if ai.elite_modifier == "Aggressive":
                weights["attack"] *= 1.3
                weights["move_to_target"] *= 1.2
            elif ai.elite_modifier == "Tactical":
                weights["use_skill"] *= 1.5
            elif ai.elite_modifier == "Frenzied":
                weights["attack"] *= 1.5
                weights["retreat"] = 0
            elif ai.elite_modifier == "Coward":
                weights["retreat"] *= 2.0
        
        # Apply situational modifiers
        health_percent = health.current / health.max if health.max > 0 else 1.0
        
        # Low health increases retreat score
        if health_percent < 0.3:
            weights["retreat"] *= 2.0
            weights["attack"] *= 0.5
        
        # Score all possible actions
        actions = []
        
        # Attack action
        attack_score = self._score_attack(entity_id, player_id)
        if attack_score > 0:
            actions.append(ActionScore(
                "attack",
                attack_score * weights["attack"],
                target_id=player_id,
            ))
        
        # Move to target action
        move_score = self._score_move_to_target(entity_id, player_id)
        if move_score > 0:
            actions.append(ActionScore(
                "move_to_target",
                move_score * weights["move_to_target"],
                target_id=player_id,
            ))
        
        # Use skill action
        if skills and skills.active:
            skill_score, skill_data = self._score_use_skill(entity_id, player_id)
            if skill_score > 0:
                actions.append(ActionScore(
                    "use_skill",
                    skill_score * weights["use_skill"],
                    target_id=player_id,
                    data=skill_data,
                ))
        
        # Retreat action
        retreat_score = self._score_retreat(entity_id, player_id)
        if retreat_score > 0:
            actions.append(ActionScore(
                "retreat",
                retreat_score * weights["retreat"],
            ))
        
        # Wait action (default)
        actions.append(ActionScore("wait", 0.3))
        
        # Return highest scored action
        if actions:
            return max(actions, key=lambda a: a.score)
        return ActionScore("wait", 0.5)

    def _score_attack(self, entity_id: int, target_id: Optional[int]) -> float:
        """Score the attack action."""
        if not target_id:
            return 0.0
        
        entity_pos = self.em.get_component(entity_id, "position")
        target_pos = self.em.get_component(target_id, "position")
        
        if not entity_pos or not target_pos:
            return 0.0
        
        # Check if in melee range
        distance = abs(entity_pos.x - target_pos.x) + abs(entity_pos.y - target_pos.y)
        
        if distance <= 1:
            return 1.0  # Can attack directly
        return 0.3  # Want to be in melee range

    def _score_move_to_target(self, entity_id: int, target_id: Optional[int]) -> float:
        """Score moving toward target."""
        if not target_id:
            return 0.0
        
        entity_pos = self.em.get_component(entity_id, "position")
        target_pos = self.em.get_component(target_id, "position")
        
        if not entity_pos or not target_pos:
            return 0.0
        
        distance = abs(entity_pos.x - target_pos.x) + abs(entity_pos.y - target_pos.y)
        
        # Higher score when far from target
        if distance > 1:
            return min(1.0, distance / 5.0)
        return 0.2  # Already adjacent

    def _score_use_skill(self, entity_id: int, target_id: Optional[int]) -> tuple[float, dict]:
        """Score using a skill."""
        if not target_id:
            return 0.0, {}
        
        skills = self.em.get_component(entity_id, "skills")
        cooldowns = self.em.get_component(entity_id, "cooldowns")
        energy = self.em.get_component(entity_id, "energy")
        entity_pos = self.em.get_component(entity_id, "position")
        target_pos = self.em.get_component(target_id, "position")
        
        if not skills or not cooldowns or not energy or not entity_pos or not target_pos:
            return 0.0, {}
        
        best_score = 0.0
        best_skill = {}
        
        distance = abs(entity_pos.x - target_pos.x) + abs(entity_pos.y - target_pos.y)
        
        for skill in skills.active:
            skill_id = skill.get("id", "")
            
            # Check cooldown
            if not cooldowns.is_ready(skill_id):
                continue
            
            # Check energy cost
            cost = skill.get("cost", 0)
            if energy.current < cost:
                continue
            
            # Check range
            skill_range = skill.get("range", 1)
            if distance > skill_range:
                continue
            
            # Score based on skill type and situation
            score = 0.5
            
            # AOE skills score higher with multiple targets nearby
            if skill.get("radius", 0) > 0:
                score += 0.3
            
            # High damage skills score higher when target is low
            target_health = self.em.get_component(target_id, "health")
            if target_health and target_health.percent < 0.3:
                score += 0.2
            
            if score > best_score:
                best_score = score
                best_skill = skill
        
        return best_score, best_skill

    def _score_retreat(self, entity_id: int, target_id: Optional[int]) -> float:
        """Score retreating from target."""
        if not target_id:
            return 0.0
        
        entity_pos = self.em.get_component(entity_id, "position")
        target_pos = self.em.get_component(target_id, "position")
        health = self.em.get_component(entity_id, "health")
        
        if not entity_pos or not target_pos or not health:
            return 0.0
        
        distance = abs(entity_pos.x - target_pos.x) + abs(entity_pos.y - target_pos.y)
        health_percent = health.current / health.max if health.max > 0 else 1.0
        
        # High score when low health and close to target
        if health_percent < 0.3 and distance <= 2:
            return 1.0
        elif health_percent < 0.5 and distance <= 1:
            return 0.7
        
        return 0.2
