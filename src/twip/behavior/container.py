from dataclasses import dataclass, field
from typing import ClassVar

from twip.behavior.base import Behavior


@dataclass
class Container(Behavior):
    kind: ClassVar[str] = "container"

    items: set[str] = field(default_factory=set)