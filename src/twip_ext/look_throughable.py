from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.behavior import Behavior
from twip.result import Result
from twip_ext.breakable import Breakable
from twip_ext.shuttered import Shuttered


@dataclass
class LookThroughable(Behavior):
    kind: ClassVar[str] = "look_throughable"

    view_message: str
    broken_view_message: str | None = None

    def handle(self, action, entity, world):
        if action.verb != "look":
            return None

        if action.preposition != "through":
            return None

        shuttered = entity.behaviors.get(Shuttered.kind)
        if isinstance(shuttered, Shuttered) and not shuttered.open:
            return Result.failure(shuttered.closed_message)

        breakable = entity.behaviors.get(Breakable.kind)
        if (
            isinstance(breakable, Breakable)
            and breakable.broken
            and self.broken_view_message is not None
        ):
            return Result.success(self.broken_view_message)

        return Result.success(self.view_message)


def register() -> None:
    pass