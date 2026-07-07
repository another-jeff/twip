from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Container
from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


def handle(world: World) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    player = world.entities[world.player_id]
    container = player.behavior(Container.kind)

    if not container.items:
        return Result.success("You are carrying nothing.")

    names = sorted(
        world.entities[item_id].names[0]
        for item_id in container.items
    )

    return Result.success("You are carrying: " + ", ".join(names))