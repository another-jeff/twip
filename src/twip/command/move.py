from __future__ import annotations

from typing import TYPE_CHECKING

from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


def handle(world: World, target: str) -> Result:
    if world.current is None:
        return Result.failure("You can't go that way.")

    exits = world._matching_exits(target)

    if not exits:
        return Result.failure("You can't go that way.")

    if len(exits) > 1:
        return Result.failure(f"Which {target} way do you mean?")

    entity, connector = exits[0]

    if world._connector_blocks_movement(entity):
        return Result.failure("It's closed.")

    there = world._other_side(connector, world.current)

    if there is None:
        return Result.failure("You can't go that way.")

    world.current = there.room

    return Result.success("You go that way.")