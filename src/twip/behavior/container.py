from dataclasses import dataclass
from typing import ClassVar

from twip.behavior.base import Behavior


@dataclass
class Container(Behavior):
    kind: ClassVar[str] = "container"