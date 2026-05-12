"""
TURNBOUND - Entity Manager (ECS-Lite)
Entity-Component System with integer IDs and archetype-based queries
"""

from typing import Dict, Any, Set, List, Optional
from dataclasses import dataclass


@dataclass
class Component:
    """Base component marker"""
    pass


class EntityManager:
    """
    ECS-Lite Entity Manager
    - Entities are integer IDs
    - Components are data-only objects
    - Systems contain logic
    """
    
    def __init__(self):
        self._next_id: int = 1
        self._components: Dict[int, Dict[str, Any]] = {}
        self._archetypes: Dict[str, Set[int]] = {}
    
    def create_entity(self) -> int:
        """Create a new entity and return its ID"""
        eid = self._next_id
        self._next_id += 1
        self._components[eid] = {}
        self._update_archetype(eid)
        return eid
    
    def add_component(self, eid: int, name: str, component: Any) -> None:
        """Add a component to an entity"""
        if eid not in self._components:
            raise ValueError(f"Entity {eid} does not exist")
        self._components[eid][name] = component
        self._update_archetype(eid)
    
    def remove_component(self, eid: int, name: str) -> Optional[Any]:
        """Remove a component from an entity"""
        if eid in self._components and name in self._components[eid]:
            comp = self._components[eid].pop(name)
            self._update_archetype(eid)
            return comp
        return None
    
    def get_component(self, eid: int, name: str) -> Optional[Any]:
        """Get a component from an entity"""
        return self._components.get(eid, {}).get(name)
    
    def has_component(self, eid: int, name: str) -> bool:
        """Check if an entity has a specific component"""
        return eid in self._components and name in self._components[eid]
    
    def remove_entity(self, eid: int) -> None:
        """Remove an entity and all its components"""
        if eid in self._components:
            del self._components[eid]
            self._rebuild_archetypes()
    
    def _update_archetype(self, eid: int) -> None:
        """Update archetype index for an entity"""
        self._rebuild_archetypes()
    
    def _rebuild_archetypes(self) -> None:
        """Rebuild archetype index (simplified approach)"""
        self._archetypes = {}
        for eid, comps in self._components.items():
            archetype_key = ",".join(sorted(comps.keys()))
            if archetype_key not in self._archetypes:
                self._archetypes[archetype_key] = set()
            self._archetypes[archetype_key].add(eid)
    
    def query_components(self, required: List[str]) -> List[int]:
        """Query entities that have all required components"""
        results = []
        required_set = set(required)
        
        for eid, comps in self._components.items():
            if required_set.issubset(set(comps.keys())):
                results.append(eid)
        
        return results
    
    def query_single(self, required: List[str]) -> Optional[int]:
        """Query for a single entity with required components"""
        results = self.query_components(required)
        return results[0] if results else None
    
    def count(self) -> int:
        """Return total number of entities"""
        return len(self._components)
    
    def clear(self) -> None:
        """Remove all entities and reset state"""
        self._components.clear()
        self._archetypes.clear()
        self._next_id = 1
    
    def get_all_entities(self) -> List[int]:
        """Get all entity IDs"""
        return list(self._components.keys())
    
    def entity_exists(self, eid: int) -> bool:
        """Check if an entity exists"""
        return eid in self._components
