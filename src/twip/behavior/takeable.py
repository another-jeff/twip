from dataclasses import dataclass
from typing import ClassVar

from twip.behavior.base import Behavior


@dataclass
class Takeable(Behavior):
    kind: ClassVar[str] = "takeable"