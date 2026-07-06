# src/twip/extension/touchable.py

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class Touchable(Component):
    message: str

    kind: ClassVar[str] = "touchable"

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != "touch":
            return None

        return Result.success(self.message)