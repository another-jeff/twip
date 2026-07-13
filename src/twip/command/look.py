from __future__ import annotations

from typing import TYPE_CHECKING

from twip.behavior import Container, Lookable, Openable
from twip.result import Result

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.parser import Action
    from twip.world import World


def room(world: World) -> Result:
    if not world.current:
        return Result.failure("You are nowhere.")

    entity = world.entities[world.current]
    lookable = entity.behaviors.get(Lookable.kind)
    description = (
        lookable.text
        if isinstance(lookable, Lookable)
        else None
    )
    contents = world.contents_of(entity)

    return Result.success(
        world.language.room(entity, description, contents)
    )


def target(world: World, action: Action) -> Result:
    matching_entities = world.find_all(action.target)

    if world.player_id:
        player = world.entities[world.player_id]
        inventory_matches = [
            entity
            for entity in world.contents_of(player)
            if entity.matches(action.target)
        ]
        matching_entities.extend(inventory_matches)

    matching_entities = list(
        {
            entity.id: entity
            for entity in matching_entities
        }.values()
    )

    if not matching_entities:
        return Result.failure(
            world.language.not_seen(action.target)
        )

    if len(matching_entities) > 1:
        return Result.failure(f"Which {action.target}?")

    entity = matching_entities[0]

    if action.preposition == "in":
        return _inside(world, entity)

    result = entity.handle(action, world)

    if result:
        return result

    return Result.failure("You can't do that.")


def _inside(world: World, entity: Entity) -> Result:
    container = entity.behaviors.get(Container.kind)

    if not isinstance(container, Container):
        return Result.failure(
            world.language.look_in_not_container(entity)
        )

    openable = entity.behaviors.get(Openable.kind)

    if (
        isinstance(openable, Openable)
        and openable.is_closed
    ):
        return Result.failure(
            world.language.look_in_closed(entity)
        )

    contents = world.contents_of(entity)

    if not contents:
        return Result.success(
            world.language.look_in_empty(entity)
        )

    return Result.success(
        world.language.look_in_contents(entity, contents)
    )