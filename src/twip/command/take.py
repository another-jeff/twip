from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Containable, Container, Takeable
from twip.result import Result

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


def handle(world: World, target: str) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    player = world.entities[world.player_id]
    player_container = player.behavior(Container.kind)

    matching_entities = [
        entity
        for entity in world.find_reachable_all(target)
        if entity.id not in player_container.items
    ]

    if not matching_entities:
        return Result.failure(
            world.language.not_seen(target)
        )

    if len(matching_entities) > 1:
        return Result.failure(f"Which {target}?")

    entity = matching_entities[0]

    if (
        Containable.kind not in entity.behaviors
        or Takeable.kind not in entity.behaviors
    ):
        return Result.failure(f"You can't take {target}.")

    containable = entity.behavior(Containable.kind)
    source: Entity | None = None

    if containable.parent and containable.parent != world.current:
        source = world.entities[containable.parent]

    world.contain(player, entity)

    return Result.success(
        world.language.take_success(entity, source)
    )