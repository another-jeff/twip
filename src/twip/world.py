from __future__ import annotations

from dataclasses import dataclass, field

from twip.component import Component
from twip.entity import Entity
from twip.extension.connector import Connector
from twip.parser import Parser
from twip.result import Result


Connection = tuple[Entity | str, str | set[str]]


@dataclass
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    parser: Parser = field(default_factory=Parser)
    current: str | None = None
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

        id = self._next_id()
        entity._assign_id(id)
        self.entities[id] = entity

        return entity

    def _next_id(self) -> str:
        id = f"entity_{self._next_entity_id}"
        self._next_entity_id += 1
        return id

    def entity(self, id: str) -> Entity:
        return self.entities[id]

    def handle(self, text: str) -> Result:
        action = self.parser.parse(text)

        if not action.verb:
            return Result.failure("Nothing happens.")

        if not action.target:
            return Result.failure(f"{action.verb.capitalize()} what?")

        matching_entities = self.find_all(action.target)

        if not matching_entities:
            return Result.failure(f"You don't see {action.target} here.")

        if len(matching_entities) > 1:
            return Result.failure(f"Which {action.target} do you mean?")

        entity = matching_entities[0]

        result = entity.handle(action, self)

        if result is None:
            return Result.failure("You can't do that.")

        return result

    def find(self, target: str) -> Entity | None:
        matching_entities = self.find_all(target)

        if len(matching_entities) == 1:
            return matching_entities[0]

        return None

    def find_all(self, target: str) -> list[Entity]:
        return [
            entity
            for entity in self.entities.values()
            if self._visible_matches(entity, target)
        ]

    def _visible_matches(self, entity: Entity, target: str) -> bool:
        if self.current is None:
            return entity.matches(target)

        if not entity.has_component(Connector.id):
            return entity.matches(target)

        connector = entity.component(Connector.id)

        if not isinstance(connector, Connector):
            return False

        side = connector.side_for(self.current)

        if side is None:
            return False

        return entity.matches(target, traits=side.traits)