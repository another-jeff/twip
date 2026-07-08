from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.behavior import Behavior


@dataclass
class Blindered(Behavior):
    kind: ClassVar[str] = "blindered"

    raised: bool = False
    open: bool = False

    closed_message: str = "The blinds are closed."
    open_view_message: str | None = None

    def handle(self, action, entity, world):
        return None


def register() -> None:
    pass