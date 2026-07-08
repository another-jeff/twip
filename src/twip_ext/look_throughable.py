from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.behavior import Behavior
from twip.result import Result
from twip_ext.breakable import Breakable
from twip_ext.view_covering import ViewCovering


def _view_covering_for(entity, world):
    for behavior in entity.behaviors.values():
        if isinstance(behavior, ViewCovering):
            return behavior

    for other in world.entities.values():
        for behavior in other.behaviors.values():
            if (
                isinstance(behavior, ViewCovering)
                and behavior.covers == entity.id
            ):
                return behavior

    return None


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

        view_covering = _view_covering_for(entity, world)
        if isinstance(view_covering, ViewCovering):
            if view_covering.blocks_view():
                return Result.failure(view_covering.closed_message)

        breakable = entity.behaviors.get(Breakable.kind)
        if (
            isinstance(breakable, Breakable)
            and breakable.broken
            and self.broken_view_message is not None
        ):
            return Result.success(self.broken_view_message)

        if (
            isinstance(view_covering, ViewCovering)
            and view_covering.changes_view()
        ):
            return Result.success(view_covering.open_view_message)

        return Result.success(self.view_message)


def register() -> None:
    pass