from __future__ import annotations

from typing import TYPE_CHECKING

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

    matching_entities = [
        entity
        for entity in world.contents_of(player)
        if world._matches(entity, target)
    ]

    if not matching_entities:
        return Result.failure(
            world.language.not_carried(target)
        )

    if len(matching_entities) > 1:
        return Result.failure(f"Which {target}?")

    entity = matching_entities[0]

    world.put(room, entity)

    return Result.success("Dropped.")