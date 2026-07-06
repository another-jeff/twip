# src/twip/extension/message_action.py

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.result import Result


@dataclass
class MessageAction(Component):
    message: str

    verb: ClassVar[str]

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != self.verb:
            return None

        return Result.success(self.message)