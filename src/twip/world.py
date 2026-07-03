from __future__ import annotations

from dataclasses import dataclass, field

from twip.entity import Entity
from twip.parser import Parser
from twip.result import Result


@dataclass
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    parser: Parser = field(default_factory=Parser)

    def add(self, entity: Entity) -> None:
        self.entities[entity.key] = entity

    def entity(self, key: str) -> Entity:
        return self.entities[key]

    def handle(self, text: str) -> Result:
        action = self.parser.parse(text)

        if not action.verb:
            return Result.failure("Nothing happens.")

        if not action.target:
            return Result.failure(f"{action.verb.capitalize()} what?")

        entity = self.find(action.target)

        if entity is None:
            return Result.failure(f"You don't see {action.target} here.")

        result = entity.handle(action, self)

        if result is None:
            return Result.failure("You can't do that.")

        return result

    def find(self, target: str) -> Entity | None:
        matching_entities = [
            entity
            for entity in self.entities.values()
            if entity.matches(target)
        ]

        if len(matching_entities) == 1:
            return matching_entities[0]

        return None