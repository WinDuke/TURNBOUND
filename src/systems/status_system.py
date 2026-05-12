from src.components.statuses import StatusEffect

class StatusSystem:
    """Система управления статус-эффектами."""
    
    # Определения всех статус-эффектов
    STATUS_DEFINITIONS = {
        "burn": {
            "name": "Burn",
            "damage_per_turn": 3,
            "damage_type": "fire",
            "description": "Deals fire damage every turn"
        },
        "poison": {
            "name": "Poison",
            "damage_per_turn": 2,
            "damage_type": "poison",
            "stacks": True,
            "description": "Stacking poison damage over time"
        },
        "shock": {
            "name": "Shock",
            "damage_multiplier": 1.5,
            "one_time": True,
            "description": "Next damage instance is increased"
        },
        "freeze": {
            "name": "Freeze",
            "skip_turn_chance": 0.5,
            "description": "Chance to skip turn"
        },
        "bleed": {
            "name": "Bleed",
            "damage_on_move": 3,
            "damage_type": "blood",
            "description": "Damage when moving"
        },
        "vulnerable": {
            "name": "Vulnerable",
            "damage_taken_mult": 1.5,
            "description": "Take increased damage"
        },
        "weakness": {
            "name": "Weakness",
            "damage_dealt_mult": 0.7,
            "description": "Deal reduced damage"
        }
    }
    
    def __init__(self, engine):
        self.engine = engine
    
    def tick_all(self):
        """Обработать тик всех статус-эффектов у всех сущностей."""
        entities_with_statuses = self.engine.entities.query_components(["Statuses", "Health"])
        
        for eid in entities_with_statuses:
            statuses_comp = self.engine.entities.get_component(eid, "Statuses")
            if not statuses_comp:
                continue
            
            # Тик длительности и получение истекших эффектов
            expired = statuses_comp.tick()
            
            # Обработка истекших one-time эффектов
            for eff in expired:
                if eff.id in self.STATUS_DEFINITIONS:
                    def_data = self.STATUS_DEFINITIONS[eff.id]
                    if def_data.get("one_time", False):
                        # Применение эффекта при истечении
                        self._apply_one_time_effect(eid, eff)
            
            # Обработка активных эффектов (DoT и др.)
            active_statuses = statuses_comp.active
            for status in active_statuses:
                self._apply_status_tick(eid, status)
    
    def _apply_status_tick(self, entity_id: int, status: StatusEffect):
        """Применить эффект тика статуса."""
        if status.id not in self.STATUS_DEFINITIONS:
            return
        
        def_data = self.STATUS_DEFINITIONS[status.id]
        
        # DoT урон (Burn, Poison)
        if "damage_per_turn" in def_data:
            dmg = def_data["damage_per_turn"] * status.stacks
            dmg_type = def_data.get("damage_type", "physical")
            
            # Учет стаков для poison
            if status.id == "poison":
                dmg = def_data["damage_per_turn"] + (status.stacks - 1)
            
            self.engine.combat.apply_damage(
                entity_id, 
                int(dmg), 
                dmg_type,
                source_id=status.source_id
            )
        
        # Проверка на пропуск хода (Freeze)
        if status.id == "freeze":
            import random
            if random.random() < def_data.get("skip_turn_chance", 0.5):
                # Пропуск хода реализуется через флаг в AI или input системе
                pass
        
        # Bleed при движении обрабатывается в movement system
    
    def _apply_one_time_effect(self, entity_id: int, status: StatusEffect):
        """Применить одноразовый эффект при истечении."""
        if status.id == "shock":
            # Shock уже применен как модификатор урона в combat system
            pass
    
    def apply_status(
        self, 
        target_id: int, 
        status_id: str, 
        duration: int, 
        stacks: int = 1,
        source_id: int = 0
    ) -> bool:
        """Наложить статус-эффект на цель."""
        if status_id not in self.STATUS_DEFINITIONS:
            return False
        
        statuses_comp = self.engine.entities.get_component(target_id, "Statuses")
        if not statuses_comp:
            return False
        
        effect = StatusEffect(
            id=status_id,
            duration=duration,
            stacks=stacks,
            source_id=source_id
        )
        
        statuses_comp.add(effect)
        
        self.engine.events.trigger("on_status_apply", {
            "target": target_id,
            "status": status_id,
            "duration": duration,
            "stacks": stacks,
            "source": source_id
        })
        
        return True
    
    def remove_status(self, target_id: int, status_id: str) -> bool:
        """Удалить статус-эффект с цели."""
        statuses_comp = self.engine.entities.get_component(target_id, "Statuses")
        if not statuses_comp:
            return False
        
        if statuses_comp.remove(status_id):
            self.engine.events.trigger("on_status_remove", {
                "target": target_id,
                "status": status_id
            })
            return True
        
        return False
    
    def has_status(self, entity_id: int, status_id: str) -> bool:
        """Проверить наличие статуса у сущности."""
        statuses_comp = self.engine.entities.get_component(entity_id, "Statuses")
        if not statuses_comp:
            return False
        return statuses_comp.has(status_id)
    
    def check_status_interactions(self, entity_id: int):
        """
        Проверить комбинации статус-эффектов для специальных взаимодействий.
        Burn + Poison = Explosion
        Shock + Wet = Chain Lightning
        Freeze + Heavy Hit = Shatter
        Blood + Fire = Burning Pools
        """
        statuses_comp = self.engine.entities.get_component(entity_id, "Statuses")
        if not statuses_comp:
            return
        
        active_ids = [s.id for s in statuses_comp.active]
        
        # Burn + Poison = Explosion
        if "burn" in active_ids and "poison" in active_ids:
            self._trigger_explosion_dot(entity_id)
        
        # Другие комбинации можно добавить здесь
    
    def _trigger_explosion_dot(self, entity_id: int):
        """Триггер взрыва от комбинации Burn + Poison."""
        # Удаляем оба статуса
        self.remove_status(entity_id, "burn")
        self.remove_status(entity_id, "poison")
        
        # Наносим урон по области (упрощенно - только цели)
        from src.components.position import Position
        pos = self.engine.entities.get_component(entity_id, "Position")
        if pos:
            # Поиск соседей
            neighbors = self.engine.entities.query_components(["Position", "Health"])
            for nid in neighbors:
                npos = self.engine.entities.get_component(nid, "Position")
                if npos and abs(npos.x - pos.x) + abs(npos.y - pos.y) <= 1:
                    self.engine.combat.apply_damage(nid, 10, "fire", entity_id)
        
        self.engine.events.trigger("on_status_interaction", {
            "type": "burn_poison_explosion",
            "entity": entity_id
        })
