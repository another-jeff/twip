from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Container, Openable
from twip.result import Result

if TYPE_CHECKING:
    from twip.action import Action
    from twip.world import World


def handle(world: World, action: Action) -> Result:
    if not world.player_id:
        return Result.failure("There is no player.")

    target = action.target

    if not target:
        return Result.failure("Put what?")

    player = world.entities[world.player_id]
    inventory = player.behavior(Container.kind)

    matching_items = [
        world.entities[item_id]
        for item_id in inventory.items
        if world._matches(
            world.entities[item_id],
            target,
        )
    ]

    if not matching_items:
        return Result.failure(
            world.language.not_carried(target)
        )

    if len(matching_items) > 1:
        return Result.failure(
            f"Which {target} do you mean?"
        )

    item = matching_items[0]

    if not action.preposition or not action.target_indirect:
        return Result.failure(
            world.language.put_missing_destination(item)
        )

    if action.preposition not in {"in", "into"}:
        return Result.failure(
            world.language.put_unsupported_relation(item)
        )

    destination_target = action.target_indirect
    matching_destinations = world.find_reachable_all(
        destination_target
    )

    if not matching_destinations:
        return Result.failure(
            world.language.not_seen(destination_target)
        )

    if len(matching_destinations) > 1:
        return Result.failure(
            f"Which {destination_target} do you mean?"
        )

    destination = matching_destinations[0]
    container = destination.behaviors.get(Container.kind)

    if not isinstance(container, Container):
        return Result.failure(
            world.language.put_in_not_container(destination)
        )

    openable = destination.behaviors.get(Openable.kind)

    if isinstance(openable, Openable) and openable.is_closed:
        return Result.failure(
            world.language.put_in_closed(destination)
        )

    world.put(destination, item)

    return Result.success(
        world.language.put_in_success(item, destination)
    )