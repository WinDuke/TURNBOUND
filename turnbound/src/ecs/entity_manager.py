"""ECS-Lite entity management system."""

from dataclasses import dataclass, field
from typing import Any


class EntityManager:
    """Manages entities and their components."""

    def __init__(self):
        self._next_id = 0
        self._entities: set[int] = set()
        self._components: dict[int, dict[str, Any]] = {}

    def create_entity(self) -> int:
        """Create a new entity and return its ID."""
        entity_id = self._next_id
        self._next_id += 1
        self._entities.add(entity_id)
        self._components[entity_id] = {}
        return entity_id

    def destroy_entity(self, entity_id: int) -> None:
        """Destroy an entity and remove all its components."""
        if entity_id in self._entities:
            self._entities.remove(entity_id)
            del self._components[entity_id]

    def add_component(self, entity_id: int, component_name: str, component: Any) -> None:
        """Add a component to an entity."""
        if entity_id in self._components:
            self._components[entity_id][component_name] = component

    def remove_component(self, entity_id: int, component_name: str) -> None:
        """Remove a component from an entity."""
        if entity_id in self._components:
            self._components[entity_id].pop(component_name, None)

    def get_component(self, entity_id: int, component_name: str) -> Any | None:
        """Get a component from an entity."""
        return self._components.get(entity_id, {}).get(component_name)

    def has_component(self, entity_id: int, component_name: str) -> bool:
        """Check if an entity has a component."""
        return component_name in self._components.get(entity_id, {})

    def get_all_entities(self) -> set[int]:
        """Get all active entities."""
        return self._entities.copy()

    def get_entities_with_components(self, *component_names: str) -> list[int]:
        """Get entities that have all specified components."""
        result = []
        for entity_id in self._entities:
            if all(
                component_name in self._components.get(entity_id, {})
                for component_name in component_names
            ):
                result.append(entity_id)
        return result

    def clear(self) -> None:
        """Clear all entities and components."""
        self._entities.clear()
        self._components.clear()
        self._next_id = 0


@dataclass
class ComponentStore:
    """Storage for a specific component type across all entities."""

    component_type: type
    _data: dict[int, Any] = field(default_factory=dict)

    def add(self, entity_id: int, component: Any) -> None:
        """Add a component for an entity."""
        self._data[entity_id] = component

    def remove(self, entity_id: int) -> None:
        """Remove a component from an entity."""
        self._data.pop(entity_id, None)

    def get(self, entity_id: int) -> Any | None:
        """Get a component for an entity."""
        return self._data.get(entity_id)

    def has(self, entity_id: int) -> bool:
        """Check if an entity has this component."""
        return entity_id in self._data

    def items(self) -> list[tuple[int, Any]]:
        """Get all entity-component pairs."""
        return list(self._data.items())

    def clear(self) -> None:
        """Clear all components."""
        self._data.clear()
