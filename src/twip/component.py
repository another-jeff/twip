from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from twip.action import Action
from twip.result import Result

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


class Component:
    key: ClassVar[str] = "component"

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        return None