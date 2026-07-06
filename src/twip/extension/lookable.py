from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class Lookable(Component):
    text: str
    verbs: FrozenSet[str] = frozenset(("look", "examine"))
    id: str = "lookable"

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: object,
    ) -> Result | None:
        if action.verb not in self.verbs:
            return None

        return Result.success(self.text)