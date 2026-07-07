# src/twip_ext/look_throughable.py

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from twip.action import Action
from twip.behavior import Behavior
from twip.result import Result
from twip_ext.breakable import Breakable

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


@dataclass
class LookThroughable(Behavior):
    kind: ClassVar[str] = "look-throughable"

    blocked_message: str
    view_message: str

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: World,
    ) -> Result | None:
        if action.verb != "look":
            return None

        if action.preposition != "through":
            return None

        breakable = entity.behaviors.get(Breakable.kind)

        if isinstance(breakable, Breakable) and breakable.broken:
            return Result.success(self.view_message)

        return Result.failure(self.blocked_message)


def register() -> None:
    pass