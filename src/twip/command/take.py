from __future__ import annotations

from typing import TYPE_CHECKING

from twip.extension import Containable, Container
from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


def handle(world: World, target: str) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    player = world.entities[world.player_id]
    player_container = player.component(Container.kind)

    matching_entities = world.find_all(target)

    if not matching_entities:
        return Result.failure(f"You don't see {target} here.")

    if len(matching_entities) > 1:
        return Result.failure(f"Which {target}?")

    entity = matching_entities[0]

    if Containable.kind not in entity.components:
        return Result.failure(f"You can't take {target}.")

    containable = entity.component(Containable.kind)

    if containable.parent:
        parent = world.entities[containable.parent]
        parent_container = parent.component(Container.kind)
        parent_container.items.remove(entity.id)

    player_container.items.add(entity.id)
    containable.parent = player.id

    return Result.success("Taken.")