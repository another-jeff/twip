from dataclasses import dataclass, field

from twip.component import Component


@dataclass
class Container(Component):
    id = "container"

    items: set[str] = field(default_factory=set)