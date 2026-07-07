from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Container, Lookable
from twip.result import Result

if TYPE_CHECKING:
    from twip.parser import Action
    from twip.world import World


def room(world: World) -> Result:
    if not world.current:
        return Result.failure("You are nowhere.")

    room = world.entities[world.current]
    message = f"You are in {room.names[-1]}."

    lookable = room.behaviors.get(Lookable.kind)

    if lookable:
        message += f" {lookable.text}"

    container = room.behaviors.get(Container.kind)

    if container and container.items:
        names = sorted(
            world.entities[item_id].names[0]
            for item_id in container.items
        )
        message += f" You see {', '.join(names)} here."

    return Result.success(message)


def target(world: World, action: Action) -> Result:
    matching_entities = world.find_all(action.target)

    if world.player_id:
        player = world.entities[world.player_id]
        inventory = player.behaviors.get(Container.kind)

        if inventory:
            inventory_matches = [
                world.entities[item_id]
                for item_id in inventory.items
                if world.entities[item_id].matches(action.target)
            ]

            matching_entities.extend(inventory_matches)

    matching_entities = list({
        entity.id: entity
        for entity in matching_entities
    }.values())

    if not matching_entities:
        return Result.failure(f"You don't see {action.target} here.")

    if len(matching_entities) > 1:
        return Result.failure(f"Which {action.target}?")

    entity = matching_entities[0]
    result = entity.handle(action, world)

    if result:
        return result

    return Result.failure("You can't do that.")