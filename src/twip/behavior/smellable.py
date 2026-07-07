# src/twip/behavior/smellable.py

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.behavior.base import Behavior
from twip.entity import Entity
from twip.result import Result


@dataclass
class Smellable(Behavior):
    message: str

    kind: ClassVar[str] = "smellable"

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != "smell":
            return None

        return Result.success(self.message)