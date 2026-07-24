from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from twip.action import Action
from twip.behavior.base import Behavior
from twip.behavior.lockable import Lockable, LockState
from twip.entity import Entity
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

    def handle(
        self,
        action: Action,
        entity: Entity,
        world,
    ) -> Result | None:
        if action.verb == "open":
            return self.change_state(
                entity,
                world,
                target_state=OpenState.OPEN,
            )

        if action.verb == "close":
            return self.change_state(
                entity,
                world,
                target_state=OpenState.CLOSED,
            )

        return None

    def change_state(
        self,
        entity: Entity,
        world,
        *,
        target_state: OpenState,
    ) -> Result:
        result = self.validate_state(entity, world, target_state)
        if result is not None:
            return result

        self.set_state(target_state)

        return self.report_state_change(entity, world, target_state)
    
    def validate_state(
        self,
        entity: Entity,
        world,
        target_state: OpenState,
    ) -> Result | None:
        if self.state == target_state:
            if target_state == OpenState.OPEN:
                return Result.success(
                    world.language.already_open(entity)
                )

            return Result.success(
                world.language.already_closed(entity)
            )

        if target_state == OpenState.OPEN:
            lockable = entity.behaviors.get(Lockable.kind)

            if (
                lockable is not None
                and lockable.state == LockState.LOCKED
            ):
                return Result.failure(
                    world.language.locked(entity)
                )

        return None

    def set_state(self, state: OpenState) -> None:
        self.state = state

    def report_state_change(
        self,
        entity: Entity,
        world,
        state: OpenState,
    ) -> Result:
        if state == OpenState.OPEN:
            return Result.success(
                world.language.open_success(entity)
            )

        return Result.success(
            world.language.close_success(entity)
        )