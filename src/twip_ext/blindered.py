from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from twip_ext.view_covering import ViewCovering


@dataclass
class Blindered(ViewCovering):
    kind: ClassVar[str] = "blindered"

    raised: bool = False

    def __post_init__(self):
        self.covering = not self.raised


def register() -> None:
    pass