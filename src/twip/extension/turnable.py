# src/twip/extension/turnable.py

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class Turnable(Component):
    message: str

    kind: ClassVar[str] = "turnable"

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != "turn":
            return None

        return Result.success(self.message)