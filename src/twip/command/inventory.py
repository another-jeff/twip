from __future__ import annotations

from typing import TYPE_CHECKING

from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


def handle(world: World) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    player = world.entities[world.player_id]
    items = world.contents_of(player)

    if not items:
        return Result.success(
            world.language.inventory_empty()
        )

    return Result.success(
        world.language.inventory_contents(items)
    )