from __future__ import annotations

from dataclasses import dataclass, field

from twip.entity import Entity
from twip.parser import Parser
from twip.result import Result


@dataclass
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    parser: Parser = field(default_factory=Parser)
    _next_entity_id: int = 1

    def add(self, entity: Entity) -> Entity:
        if entity.has_key:
            raise ValueError(f"Entity already has key: {entity.key}")

        key = self._next_key()
        entity._assign_key(key)
        self.entities[key] = entity

        return entity

    def _next_key(self) -> str:
        key = f"entity_{self._next_entity_id}"
        self._next_entity_id += 1
        return key

    def entity(self, key: str) -> Entity:
        return self.entities[key]

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
            if entity.matches(target)
        ]