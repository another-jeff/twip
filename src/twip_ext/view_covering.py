from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip.behavior import Behavior
from twip.result import Result


@dataclass
class ViewCovering(Behavior):
    kind: ClassVar[str] = "view_covering"

    covers: str | None = None

    # Is the covering currently in front of the view?
    covering: bool = True

    # If it is still covering, can you see through/around it?
    open: bool = False

    closed_message: str = "The view is covered."
    open_view_message: str | None = None

    open_message: str = "You open it."
    close_message: str = "You close it."

    # Curtains/shutters open by uncovering the view.
    # Blinds usually open while still covering the view.
    open_uncovers: bool = False

    def handle(self, action, entity, world):
        if action.verb == "open":
            self.open = True

            if self.open_uncovers:
                self.covering = False

            return Result.success(self.open_message)

        if action.verb == "close":
            self.open = False
            self.covering = True

            return Result.success(self.close_message)

        return None

    def blocks_view(self) -> bool:
        return self.covering and not self.open

    def changes_view(self) -> bool:
        return (
            self.covering
            and self.open
            and self.open_view_message is not None
        )


def register() -> None:
    pass