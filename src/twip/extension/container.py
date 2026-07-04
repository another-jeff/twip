from dataclasses import dataclass, field

from twip.component import Component


@dataclass
class Container(Component):
    key = "container"

    items: set[str] = field(default_factory=set)