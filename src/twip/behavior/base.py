from __future__ import annotations

from typing import TYPE_CHECKING

from twip.result import Result

if TYPE_CHECKING:
    from twip.action import Action
    from twip.entity import Entity
    from twip.world import World


class Behavior:
    kind: str

    def handle(
        self,
        world: World,
        entity: Entity,
        action: Action,
    ) -> Result | None:
        return None