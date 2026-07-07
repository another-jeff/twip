from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from twip.action import Action
from twip.behavior.base import Behavior
from twip.entity import Entity
from twip.behavior.lockable import Lockable, LockState
from twip.result import Result


class OpenState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"


@dataclass
class Openable(Behavior):
    kind: ClassVar[str] = "openable"

    state: OpenState = OpenState.CLOSED

    @property
    def is_open(self) -> bool:
        return self.state == OpenState.OPEN

    @property
    def is_closed(self) -> bool:
        return self.state == OpenState.CLOSED

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb == "open":
            return self.open(entity)

        if action.verb == "close":
            return self.close(entity)

        return None

    def open(self, entity: Entity) -> Result:
        if self.is_open:
            return Result.success(f"The {entity.name} is already open.")

        lockable = entity.behaviors.get(Lockable.kind)

        if lockable is not None and lockable.state == LockState.LOCKED:
            return Result.failure(f"The {entity.name} is locked.")

        self.state = OpenState.OPEN
        return Result.success(f"You open the {entity.name}.")

    def close(self, entity: Entity) -> Result:
        if self.is_closed:
            return Result.success(f"The {entity.name} is already closed.")

        self.state = OpenState.CLOSED
        return Result.success(f"You close the {entity.name}.")