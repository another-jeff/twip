from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Container
from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


def handle(world: World, target: str) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    if not world.current:
        return Result.failure("You are nowhere.")

    player = world.entities[world.player_id]
    room = world.entities[world.current]
    player_container = player.behavior(Container.kind)

    matching_entities = [
        world.entities[item_id]
        for item_id in player_container.items
        if world._matches(world.entities[item_id], target)
    ]

    if not matching_entities:
        return Result.failure(
            world.language.not_carried(target)
        )

    if len(matching_entities) > 1:
        return Result.failure(f"Which {target}?")

    entity = matching_entities[0]
    world.contain(room, entity)

    return Result.success("Dropped.")