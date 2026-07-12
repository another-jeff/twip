from __future__ import annotations

from dataclasses import dataclass, field

from twip.behavior import Behavior
from twip.dispatcher import dispatch
from twip.entity import Entity
from twip.parser import Parser
from twip.result import Result
from twip.behavior import (
    Behavior,
    Containable,
    Container,
    Connector,
    Openable,
)

Connection = tuple[Entity | str, str | set[str]]


@dataclass
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    parser: Parser = field(default_factory=Parser)
    current: str | None = None
    player_id: str | None = None
    _next_entity_id: int = 1

    def add(
        self,
        names: tuple[str, ...],
        traits: set[str] | None = None,
        behaviors: tuple[Behavior, ...] = (),
    ) -> Entity:
        entity = Entity(
            names=names,
            traits=traits or set(),
        )

        entity.add_behavior(*behaviors)

        return self._add_entity(entity)

    def add_and_connect(
        self,
        names: tuple[str, ...],
        connections: tuple[Connection, ...],
        traits: set[str] | None = None,
        behaviors: tuple[Behavior, ...] = (),
    ) -> Entity:
        connector = Connector.from_connections(connections)

        return self.add(
            names=names,
            traits=traits,
            behaviors=(*behaviors, connector),
        )

    def _add_entity(self, entity: Entity) -> Entity:
        if entity.has_id:
            raise ValueError(f"Entity already has id: {entity.id}")

        entity_id = self._new_entity_id()
        entity._assign_id(entity_id)
        self.entities[entity_id] = entity

        return entity

    def _new_entity_id(self) -> str:
        entity_id = f"entity_{self._next_entity_id}"
        self._next_entity_id += 1
        return entity_id

    def entity(self, entity_id: str) -> Entity:
        return self.entities[entity_id]

    def handle(self, text: str) -> Result:
        action = self.parser.parse(text)
        return dispatch(self, action)

    def find(self, target: str) -> Entity | None:
        matching_entities = self.find_all(target)

        if len(matching_entities) == 1:
            return matching_entities[0]

        return None

    def find_all(self, target: str) -> list[Entity]:
        return [
            entity
            for entity in self.entities.values()
            if self._is_visible(entity)
            if self._matches(entity, target)
        ]

    def find_reachable_all(self, target: str) -> list[Entity]:
        return [
            entity
            for entity in self.entities.values()
            if self._is_reachable(entity)
            if self._matches(entity, target)
        ]

    def _is_reachable(self, entity: Entity) -> bool:
        if self._is_in_player_inventory(entity):
            return True

        if self.current is None:
            return True

        if entity.id == self.current:
            return True

        if Connector.kind in entity.behaviors:
            return self._connector_is_visible(entity)

        return self._containment_path_allows(
            entity,
            root_id=self.current,
            blocked_by=self._blocks_reach,
        )

    def _matches(self, entity: Entity, target: str) -> bool:
        if self.current is None:
            return entity.matches(target)

        if not entity.has_behavior(Connector.kind):
            return entity.matches(target)

        connector = entity.behavior(Connector.kind)

        if not isinstance(connector, Connector):
            return False

        side = connector.side_for(self.current)

        if side is None:
            return False

        return entity.matches(target, traits=side.traits)

    def _is_visible(self, entity: Entity) -> bool:
        if self.current is None:
            return True

        if entity.id == self.current:
            return True

        if Connector.kind in entity.behaviors:
            return self._connector_is_visible(entity)

        return self._containment_path_allows(
            entity,
            root_id=self.current,
            blocked_by=self._blocks_visibility,
        )

    def _connector_is_visible(self, entity: Entity) -> bool:
        connector = entity.behavior(Connector.kind)

        if not isinstance(connector, Connector):
            return False

        return connector.side_for(self.current) is not None

    def contain(self, container: Entity, entity: Entity) -> None:
        container.behaviors[Container.kind].items.add(entity.id)
        entity.behaviors[Containable.kind].parent = container.id

    def _is_in_player_inventory(self, entity: Entity) -> bool:
        if self.player_id is None:
            return False

        player = self.entities.get(self.player_id)

        if player is None:
            return False

        container = player.behaviors.get(Container.kind)

        return (
            container is not None
            and entity.id in container.items
        )
        
    def _is_visible_from(
        self,
        entity: Entity,
        root_id: str,
    ) -> bool:
        current = entity
        seen: set[str] = set()

        while True:
            containable = current.behaviors.get(Containable.kind)

            if not isinstance(containable, Containable):
                return False

            parent_id = containable.parent

            if parent_id == root_id:
                return True

            if parent_id is None or parent_id in seen:
                return False

            seen.add(parent_id)

            parent = self.entities.get(parent_id)

            if parent is None:
                return False

            openable = parent.behaviors.get(Openable.kind)

            if (
                isinstance(openable, Openable)
                and not openable.is_open
            ):
                return False

            current = parent
            
    def _containment_path_allows(
        self,
        entity: Entity,
        *,
        root_id: str,
        blocked_by: Callable[[Entity], bool],
    ) -> bool:
        current = entity
        seen: set[str] = set()

        while True:
            containable = current.behaviors.get(Containable.kind)

            if not isinstance(containable, Containable):
                return False

            parent_id = containable.parent

            if parent_id == root_id:
                return True

            if parent_id is None or parent_id in seen:
                return False

            seen.add(parent_id)

            parent = self.entities.get(parent_id)

            if parent is None:
                return False

            if blocked_by(parent):
                return False

            current = parent

    def _blocks_visibility(self, entity: Entity) -> bool:
        openable = entity.behaviors.get(Openable.kind)

        return (
            isinstance(openable, Openable)
            and openable.is_closed
        )


    def _blocks_reach(self, entity: Entity) -> bool:
        openable = entity.behaviors.get(Openable.kind)

        return (
            isinstance(openable, Openable)
            and openable.is_closed
        )