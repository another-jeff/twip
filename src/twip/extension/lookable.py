from __future__ import annotations

from dataclasses import dataclass

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class Lookable(Component):
    text: str
    id: str = "lookable"

    def handle(self, action: Action, entity: Entity, world: object) -> Result:
        if action.verb == "look":
            return Result.success(self.text)

        return Result.failure("Nothing happens.")