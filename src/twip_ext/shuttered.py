from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.behavior import Behavior


@dataclass
class Shuttered(Behavior):
    kind: ClassVar[str] = "shuttered"

    open: bool = False
    closed_message: str = "The shutters are closed."

    def handle(self, action, entity, world):
        return None


def register() -> None:
    pass