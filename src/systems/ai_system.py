"""
AI System for TURNBOUND.
Handles enemy turns using Utility AI and Pathfinding.
"""
from src.ai.pathfinding import find_path
from src.ai.utility_ai import UtilityAI

class AISystem:
    """
    Manages AI behavior for all enemies.
    Uses Utility AI to decide actions and A* for movement.
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.scorer = UtilityAI()
        
    def execute_turn(self, enemy_id: int):
        """
        Execute a single turn for an enemy entity.
        1. Get components
        2. Evaluate best action via Utility AI
        3. Execute action (Move, Attack, Skill)
        """
        player_id = self.engine.player_id
        if not player_id:
            return # No player to act against
            
        # Get enemy components
        enemy_pos = self.engine.entities.get_component(enemy_id, "Position")
        enemy_health = self.engine.entities.get_component(enemy_id, "Health")
        enemy_skills = self.engine.entities.get_component(enemy_id, "Skills")
        enemy_ai = self.engine.entities.get_component(enemy_id, "AI")
        
        if not enemy_pos or not enemy_health:
            return # Essential components missing
            
        # Check if dead
        if enemy_health.current_hp <= 0:
            return
            
        # Get player position
        player_pos = self.engine.entities.get_component(player_id, "Position")
        if not player_pos:
            return
            
        # Evaluate best action
        action = self.scorer.evaluate(
            enemy_id, 
            enemy_pos, 
            player_pos, 
            enemy_health, 
            enemy_skills, 
            self.engine
        )
        
        # Execute the chosen action
        action_type = action.get("type")
        
        if action_type == "ATTACK":
            self._perform_attack(enemy_id, player_id)
            
        elif action_type == "MOVE":
            target = action.get("target")
            if target:
                self._perform_move(enemy_id, target)
                
        elif action_type == "SKILL":
            skill_id = action.get("skill_id")
            if skill_id:
                self._perform_skill(enemy_id, skill_id, player_id)
                
        elif action_type == "RETREAT":
            target = action.get("target")
            if target:
                self._perform_move(enemy_id, target)
                
    def _perform_attack(self, attacker_id: int, target_id: int):
        """Perform a basic melee attack."""
        # Base damage 5 for now, physical type
        self.engine.combat.apply_damage(target_id, 5, "physical", False, attacker_id)
        
    def _perform_move(self, entity_id: int, target_pos: tuple):
        """Move entity towards target position using A*."""
        current_pos = self.engine.entities.get_component(entity_id, "Position")
        if not current_pos:
            return
            
        # Find path
        path = find_path(
            self.engine.current_arena["grid"], 
            (current_pos.x, current_pos.y), 
            target_pos
        )
        
        if path and len(path) > 1:
            # Take the first step (path[1] because path[0] is current pos)
            next_step = path[1]
            dx = next_step[0] - current_pos.x
            dy = next_step[1] - current_pos.y
            
            # Try to move
            self.engine.movement.move_entity(entity_id, dx, dy)
            
    def _perform_skill(self, caster_id: int, skill_id: str, target_id: int):
        """Use a skill on target."""
        target_pos_comp = self.engine.entities.get_component(target_id, "Position")
        if not target_pos_comp:
            return
            
        target_pos = (target_pos_comp.x, target_pos_comp.y)
        self.engine.combat.use_skill(caster_id, skill_id, target_pos)
