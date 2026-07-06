from dataclasses import dataclass
from typing import ClassVar

from twip.component import Component


@dataclass
class Containable(Component):
    kind: ClassVar[str] = "containable"

    parent: str | None = None