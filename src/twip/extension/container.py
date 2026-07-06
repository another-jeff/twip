from dataclasses import dataclass, field
from typing import ClassVar

from twip.component import Component


@dataclass
class Container(Component):
    kind: ClassVar[str] = "container"

    items: set[str] = field(default_factory=set)