from __future__ import annotations

from dataclasses import dataclass, field

from twip.component import Component
from twip.dispatcher import dispatch
from twip.entity import Entity
from twip.extension import Containable, Container, Connector
from twip.parser import Parser
from twip.result import Result


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
        components: tuple[Component, ...] = (),
    ) -> Entity:
        entity = Entity(
            names=names,
            traits=traits or set(),
        )

        entity.add_component(*components)

        return self._add_entity(entity)

    def add_and_connect(
        self,
        names: tuple[str, ...],
        connections: tuple[Connection, ...],
        traits: set[str] | None = None,
        components: tuple[Component, ...] = (),
    ) -> Entity:
        connector = Connector.from_connections(connections)

        return self.add(
            names=names,
            traits=traits,
            components=(*components, connector),
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

    def find_accessible_all(self, target: str) -> list[Entity]:
        return [
            entity
            for entity in self.entities.values()
            if self._is_accessible(entity)
            if self._matches(entity, target)
        ]

    def _is_accessible(self, entity: Entity) -> bool:
        return (
            self._is_visible(entity)
            or self._is_in_player_inventory(entity)
        )

    def _matches(self, entity: Entity, target: str) -> bool:
        if self.current is None:
            return entity.matches(target)

        if not entity.has_component(Connector.kind):
            return entity.matches(target)

        connector = entity.component(Connector.kind)

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

        if Connector.kind in entity.components:
            return self._connector_is_visible(entity)

        current_room = self.entity(self.current)
        container = current_room.components.get(Container.kind)

        return (
            container is not None
            and entity.id in container.items
        )

    def _connector_is_visible(self, entity: Entity) -> bool:
        connector = entity.component(Connector.kind)

        if not isinstance(connector, Connector):
            return False

        return connector.side_for(self.current) is not None

    def contain(self, container: Entity, entity: Entity) -> None:
        container.components[Container.kind].items.add(entity.id)
        entity.components[Containable.kind].parent = container.id

    def _is_in_player_inventory(self, entity: Entity) -> bool:
        if self.player_id is None:
            return False

        player = self.entities.get(self.player_id)

        if player is None:
            return False

        container = player.components.get(Container.kind)

        return (
            container is not None
            and entity.id in container.items
        )