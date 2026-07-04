from dataclasses import dataclass

from twip.component import Component


@dataclass
class Containable(Component):
    id = "containable"

    parent: str | None = None