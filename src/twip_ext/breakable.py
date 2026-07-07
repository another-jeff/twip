# src/twip_ext/breakable.py

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from twip.action import Action
from twip.behavior import Behavior
from twip.result import Result
from twip.verb import register_verb

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


@dataclass
class Breakable(Behavior):
    kind: ClassVar[str] = "breakable"

    break_message: str = "It breaks."
    already_broken_message: str = "It's already broken."
    broken: bool = False

    @classmethod
    def register_verb(cls) -> None:
        register_verb("break")

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: World,
    ) -> Result | None:
        if action.verb != "break":
            return None

        if self.broken:
            return Result.failure(self.already_broken_message)

        self.broken = True
        return Result.success(self.break_message)


def register() -> None:
    Breakable.register_verb()