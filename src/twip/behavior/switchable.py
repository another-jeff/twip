from __future__ import annotations

from enum import StrEnum
from typing import ClassVar

from twip.action import Action
from twip.behavior.base import Behavior
from twip.entity import Entity
from twip.result import Result


class SwitchState(StrEnum):
    OFF = "off"
    ON = "on"


class Switchable(Behavior):
    kind: ClassVar[str] = "switchable"

    def __init__(
        self,
        *,
        state: SwitchState = SwitchState.OFF,
    ):
        self.state = state

    @property
    def is_on(self) -> bool:
        return self.state == SwitchState.ON

    @property
    def is_off(self) -> bool:
        return self.state == SwitchState.OFF

    def handle(
        self,
        action: Action,
        entity: Entity,
        world,
    ) -> Result | None:
        if action.verb != "turn":
            return None

        if action.preposition == "on":
            return self.change_state(
                entity,
                world,
                target_state=SwitchState.ON,
            )

        if action.preposition == "off":
            return self.change_state(
                entity,
                world,
                target_state=SwitchState.OFF,
            )

        return None

    def change_state(
        self,
        entity: Entity,
        world,
        *,
        target_state: SwitchState,
    ) -> Result:
        result = self.validate_state(
            entity,
            world,
            target_state,
        )
        if result is not None:
            return result

        self.set_state(target_state)

        return self.report_state_change(
            entity,
            world,
            target_state,
        )

    def validate_state(
        self,
        entity: Entity,
        world,
        target_state: SwitchState,
    ) -> Result | None:
        if self.state != target_state:
            return None

        if target_state == SwitchState.ON:
            return Result.success(
                world.language.already_on(entity)
            )

        return Result.success(
            world.language.already_off(entity)
        )

    def set_state(self, state: SwitchState) -> None:
        self.state = state

    def report_state_change(
        self,
        entity: Entity,
        world,
        state: SwitchState,
    ) -> Result:
        if state == SwitchState.ON:
            return Result.success(
                world.language.turn_on_success(entity)
            )

        return Result.success(
            world.language.turn_off_success(entity)
        )