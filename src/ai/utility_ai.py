"""
Utility AI System for TURNBOUND.
Enemies evaluate actions dynamically based on scores.
"""
from typing import Dict, Any, List, Optional
from src.components.position import Position
from src.components.health import Health
from src.components.skills import Skills

class UtilityAI:
    """
    Evaluates possible actions for an enemy and returns the best one.
    Actions: ATTACK, MOVE, SKILL, RETREAT
    """
    
    def __init__(self):
        # Weights for scoring factors
        self.weights = {
            "distance_to_player": 1.5,
            "health_threshold": 2.0,
            "skill_available": 1.8,
            "cooldown_ready": 1.2
        }
    
    def evaluate(self, entity_id: int, my_pos: Position, player_pos: Position, 
                 my_health: Health, skills_comp: Optional[Skills], engine) -> Dict[str, Any]:
        """
        Evaluate all possible actions and return the best one.
        
        Returns dict with 'type' and optional 'target' or 'skill_id'.
        """
        scores = {
            "ATTACK": 0.0,
            "MOVE": 0.0,
            "SKILL": 0.0,
            "RETREAT": 0.0
        }
        
        # Calculate Manhattan distance
        dist = abs(my_pos.x - player_pos.x) + abs(my_pos.y - player_pos.y)
        
        # --- ATTACK Scoring ---
        # Can only attack if adjacent (dist == 1)
        if dist == 1:
            base_score = 80.0
            # Bonus if player has low HP (finish them off)
            if player_has_low_hp(engine, player_pos):
                base_score += 20.0
            scores["ATTACK"] = base_score
        else:
            scores["ATTACK"] = 0.0 # Cannot attack from range without skill
            
        # --- MOVE Scoring ---
        # Move towards player if not in attack range
        if dist > 1:
            scores["MOVE"] = 70.0 + (10.0 / max(1, dist)) # Closer = higher urgency
        else:
            scores["MOVE"] = 10.0 # Already next to player, low priority to move
            
        # --- SKILL Scoring ---
        if skills_comp and len(skills_comp.known) > 0:
            # Check for ready skills
            ready_skills = [s for s in skills_comp.known if skills_comp.cooldowns.get(s, 0) == 0]
            if ready_skills:
                # Prefer skills if in range
                # Simplified: assume skill range is 5 for now
                if dist <= 5:
                    scores["SKILL"] = 90.0
                else:
                    scores["SKILL"] = 40.0 # Not in range, but maybe AOE?
                    
        # --- RETREAT Scoring ---
        # Retreat if health is critically low (< 20%)
        health_pct = my_health.current_hp / max(1, my_health.max_hp)
        if health_pct < 0.2:
            scores["RETREAT"] = 85.0
            # Increase score if player is strong (simplified: just dist)
            if dist == 1:
                scores["RETREAT"] += 15.0 # Panic!
        else:
            scores["RETREAT"] = 5.0 # Generally don't retreat
            
        # Determine best action
        best_action = max(scores, key=scores.get)
        best_score = scores[best_action]
        
        result = {"type": best_action, "score": best_score}
        
        # Add specific data for the action
        if best_action == "SKILL" and skills_comp:
            ready_skills = [s for s in skills_comp.known if skills_comp.cooldowns.get(s, 0) == 0]
            if ready_skills:
                result["skill_id"] = ready_skills[0] # Pick first ready skill
                
        if best_action == "MOVE":
            # Target is player position
            result["target"] = (player_pos.x, player_pos.y)
            
        if best_action == "RETREAT":
            # Target is opposite direction of player (simplified: just random empty spot far away)
            # For now, target player pos but movement system will handle logic reversal if needed
            # Or better: find spot furthest from player. Simplified: just move away vector.
            result["target"] = self._get_retreat_target(my_pos, player_pos, engine)
            
        return result
        
    def _get_retreat_target(self, my_pos: Position, player_pos: Position, engine) -> tuple:
        """Calculate a target position to retreat to."""
        # Simple logic: go opposite direction
        dx = my_pos.x - player_pos.x
        dy = my_pos.y - player_pos.y
        
        # Normalize to step size 1
        if dx > 0: dx = 1
        elif dx < 0: dx = -1
        else: dx = 0
        
        if dy > 0: dy = 1
        elif dy < 0: dy = -1
        else: dy = 0
        
        target_x = my_pos.x + dx
        target_y = my_pos.y + dy
        
        # Bounds check (simplified, assuming arena size known or handled by movement)
        return (target_x, target_y)

def player_has_low_hp(engine, player_pos) -> bool:
    """Helper to check if player is low HP."""
    # Query player entity (simplified: assuming we can find it by position or stored ID)
    # In real implementation, use engine.player_id
    if hasattr(engine, 'player_id') and engine.player_id:
        p_health = engine.entities.get_component(engine.player_id, "Health")
        if p_health:
            return p_health.current_hp < (p_health.max_hp * 0.3)
    return False
