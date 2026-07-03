from dataclasses import dataclass
from enum import StrEnum

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


class DoorState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"


@dataclass
class Door(Component):
    key = "door"

    state: DoorState = DoorState.CLOSED

    @property
    def is_open(self) -> bool:
        return self.state == DoorState.OPEN

    @property
    def is_closed(self) -> bool:
        return self.state == DoorState.CLOSED

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.target not in {self.key, entity.key, entity.name.lower()}:
            return None

        if action.verb == "open":
            return self.open(entity)

        if action.verb == "close":
            return self.close(entity)

        return None

    def open(self, entity: Entity) -> Result:
        if self.is_open:
            return Result.success(f"The {entity.name} is already open.")

        self.state = DoorState.OPEN
        return Result.success(f"You open the {entity.name}.")

    def close(self, entity: Entity) -> Result:
        if self.is_closed:
            return Result.success(f"The {entity.name} is already closed.")

        self.state = DoorState.CLOSED
        return Result.success(f"You close the {entity.name}.")