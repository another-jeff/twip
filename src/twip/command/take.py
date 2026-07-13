from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Takeable
from twip.result import Result

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


def handle(world: World, target: str) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    player = world.entities[world.player_id]

    matching_entities = [
        entity
        for entity in world.find_reachable_all(target)
        if entity.parent != player.id
    ]

    if not matching_entities:
        return Result.failure(
            world.language.not_seen(target)
        )

    if len(matching_entities) > 1:
        return Result.failure(f"Which {target}?")

    entity = matching_entities[0]

    if Takeable.kind not in entity.behaviors:
        return Result.failure(
            world.language.take_not_takeable(entity)
        )

    source: Entity | None = None

    if entity.parent and entity.parent != world.current:
        source = world.entities[entity.parent]

    world.put(player, entity)

    return Result.success(
        world.language.take_success(entity, source)
    )