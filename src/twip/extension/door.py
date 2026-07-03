from dataclasses import dataclass

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class Door(Component):
    key = "door"

    is_open: bool = False

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != "open":
            return None

        if action.target not in {self.key, entity.key, entity.name.lower()}:
            return None

        if self.is_open:
            return Result.success(f"The {entity.name} is already open.")

        self.is_open = True
        return Result.success(f"You open the {entity.name}.")