from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.behavior import Behavior
from twip.result import Result


@dataclass
class Blindered(Behavior):
    kind: ClassVar[str] = "blindered"

    raised: bool = False
    open: bool = False
    covers: str | None = None

    closed_message: str = "The blinds are closed."
    open_view_message: str | None = None

    open_message: str = "You open the blinds."
    close_message: str = "You close the blinds."

    def handle(self, action, entity, world):
        if action.verb == "open":
            self.open = True
            return Result.success(self.open_message)

        if action.verb == "close":
            self.open = False
            return Result.success(self.close_message)

        return None


def register() -> None:
    pass