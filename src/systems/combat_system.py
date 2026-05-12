import random
from typing import List, Tuple, Optional, Dict, Any

class CombatSystem:
    """Система боевых расчетов и применения урона."""
    
    # Типы урона согласно спецификации
    DAMAGE_TYPES = ["physical", "fire", "frost", "lightning", "void", "poison", "blood"]
    
    def __init__(self, engine):
        self.engine = engine
        
    def calculate_damage(
        self, 
        attacker_id: int, 
        defender_id: int, 
        base_damage: int, 
        damage_type: str = "physical"
    ) -> Tuple[int, bool]:
        """
        Рассчитать урон по формуле:
        FinalDamage = (BaseDamage + Power) × CritMultiplier - Defense
        
        Возвращает (final_damage, is_crit)
        """
        atk_stats = self.engine.entities.get_component(attacker_id, "Stats")
        def_stats = self.engine.entities.get_component(defender_id, "Stats")
        
        if not atk_stats or not def_stats:
            return max(1, base_damage), False
        
        # Проверка на критический удар
        is_crit = random.random() < atk_stats.crit_chance
        crit_mult = atk_stats.crit_mult if is_crit else 1.0
        
        # Основная формула
        raw_damage = (base_damage + atk_stats.power) * crit_mult
        final_damage = max(1, int(raw_damage - def_stats.defense))
        
        # Триггер событий
        if is_crit:
            self.engine.events.trigger("on_crit", {
                "attacker": attacker_id,
                "defender": defender_id,
                "damage": final_damage
            })
        
        return final_damage, is_crit
    
    def apply_damage(
        self, 
        target_id: int, 
        amount: int, 
        damage_type: str = "physical",
        source_id: int = 0
    ) -> int:
        """
        Применить урон цели. Возвращает фактический полученный урон.
        """
        health = self.engine.entities.get_component(target_id, "Health")
        if not health:
            return 0
        
        # Применение модификаторов от статусов (уязвимость, сопротивление)
        modified_amount = self._apply_status_modifiers(target_id, amount, damage_type)
        
        # Нанесение урона
        actual_damage = health.take_damage(modified_amount)
        
        # Событие попадания
        self.engine.events.trigger("on_hit", {
            "target": target_id,
            "source": source_id,
            "damage": actual_damage,
            "damage_type": damage_type
        })
        
        # Проверка смерти
        if health.is_dead():
            self.engine.events.trigger("on_kill", {
                "killer": source_id,
                "victim": target_id
            })
            self.engine.entities.remove_entity(target_id)
        
        return actual_damage
    
    def _apply_status_modifiers(
        self, 
        target_id: int, 
        damage: int, 
        damage_type: str
    ) -> int:
        """Применить модификаторы урона от статус-эффектов."""
        statuses = self.engine.entities.get_component(target_id, "Statuses")
        if not statuses:
            return damage
        
        modifier = 1.0
        
        # Уязвимость (Vulnerable) - увеличивает получаемый урон
        if statuses.has("vulnerable"):
            vuln_effect = statuses.get("vulnerable")
            if vuln_effect:
                modifier *= 1.5  # +50% урона
        
        # Ослабление (Weakness) - уменьшает наносимый урон атакующего
        # (обрабатывается в другом месте)
        
        return int(damage * modifier)
    
    def use_skill(
        self, 
        entity_id: int, 
        skill_id: str, 
        target_pos: Tuple[int, int]
    ) -> bool:
        """
        Использовать навык.
        Возвращает True если успешно.
        """
        skills_comp = self.engine.entities.get_component(entity_id, "Skills")
        energy_comp = self.engine.entities.get_component(entity_id, "Energy")
        
        if not skills_comp:
            return False
        
        # Проверка доступности навыка
        if not skills_comp.can_use(skill_id):
            return False
        
        # Получение данных навыка
        skill_data = self.engine.content.get_skill(skill_id)
        if not skill_data:
            return False
        
        # Проверка энергии
        if energy_comp:
            cost = skill_data.get("cost", 0)
            if not energy_comp.consume(cost):
                return False
        
        # Определение целей
        targets = self._get_targets_in_range(entity_id, target_pos, skill_data)
        
        # Применение эффекта навыка
        for target_id in targets:
            if target_id == entity_id and not skill_data.get("self_target", False):
                continue
                
            dmg_type = skill_data.get("damage_type", "physical")
            base_dmg = skill_data.get("damage", 0)
            
            if base_dmg > 0:
                self.apply_damage(target_id, base_dmg, dmg_type, entity_id)
            
            # Применение статус-эффектов от навыка
            if "status_effects" in skill_data:
                self._apply_skill_statuses(target_id, skill_data["status_effects"], entity_id)
        
        # Установка кулдауна
        cooldown = skill_data.get("cooldown", 3)
        skills_comp.set_cooldown(skill_id, cooldown)
        
        # Событие использования навыка
        self.engine.events.trigger("on_skill_used", {
            "user": entity_id,
            "skill": skill_id,
            "targets": targets
        })
        
        return True
    
    def _get_targets_in_range(
        self, 
        source_id: int, 
        target_pos: Tuple[int, int], 
        skill_data: Dict[str, Any]
    ) -> List[int]:
        """Получить список целей в радиусе навыка."""
        targets = []
        
        source_pos = self.engine.entities.get_component(source_id, "Position")
        if not source_pos:
            return targets
        
        radius = skill_data.get("radius", 0)
        range_dist = skill_data.get("range", 1)
        
        # Проверка дистанции до точки цели
        dist_to_target = abs(target_pos[0] - source_pos.x) + abs(target_pos[1] - source_pos.y)
        if dist_to_target > range_dist:
            return targets  # Цель слишком далеко
        
        # Поиск всех сущностей в радиусе
        all_entities = self.engine.entities.query_components(["Position", "Health"])
        
        for eid in all_entities:
            pos = self.engine.entities.get_component(eid, "Position")
            if not pos:
                continue
            
            # Расстояние до точки цели (для AOE)
            dist = abs(pos.x - target_pos[0]) + abs(pos.y - target_pos[1])
            
            if dist <= radius:
                targets.append(eid)
        
        return targets
    
    def _apply_skill_statuses(
        self, 
        target_id: int, 
        status_list: List[Dict[str, Any]], 
        source_id: int
    ):
        """Применить статус-эффекты от навыка."""
        from src.components.statuses import StatusEffect
        
        statuses_comp = self.engine.entities.get_component(target_id, "Statuses")
        if not statuses_comp:
            return
        
        for status_info in status_list:
            effect = StatusEffect(
                id=status_info["id"],
                duration=status_info.get("duration", 3),
                stacks=status_info.get("stacks", 1),
                source_id=source_id
            )
            statuses_comp.add(effect)
            self.engine.events.trigger("on_status_apply", {
                "target": target_id,
                "status": status_info["id"],
                "source": source_id
            })
