from dataclasses import dataclass
from typing import ClassVar

from twip.behavior.base import Behavior


@dataclass
class Containable(Behavior):
    kind: ClassVar[str] = "containable"

    parent: str | None = None