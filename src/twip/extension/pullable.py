from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class Pullable(Component):
    message: str = "You pull it."

    kind: ClassVar[str] = "pullable"

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != "pull":
            return None

        return Result.success(self.message)