from __future__ import annotations

from typing import TYPE_CHECKING

from twip.entity import Entity
from twip.extension import Connector, Openable, OpenState
from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


def handle(world: World, target: str) -> Result:
    if world.current is None:
        return Result.failure("You can't go that way.")

    exits = _matching_exits(world, target)

    if not exits:
        return Result.failure("You can't go that way.")

    if len(exits) > 1:
        return Result.failure(f"Which {target} way do you mean?")

    entity, connector = exits[0]

    if _connector_blocks_movement(entity):
        return Result.failure("It's closed.")

    there = _other_side(connector, world.current)

    if there is None:
        return Result.failure("You can't go that way.")

    world.current = there.room

    return Result.success("You go that way.")


def _matching_exits(world: World, target: str) -> list[tuple[Entity, Connector]]:
    exits = []

    for entity in world.entities.values():
        connector = entity.components.get(Connector.id)

        if not isinstance(connector, Connector):
            continue

        here = connector.side_for(world.current)

        if here is None:
            continue

        if target in here.traits:
            exits.append((entity, connector))
            continue

        if not _target_mentions_side(target, here.traits):
            continue

        if entity.matches(target, traits=here.traits):
            exits.append((entity, connector))

    return exits


def _target_mentions_side(target: str, side_traits: set[str]) -> bool:
    words = set(target.split())

    return bool(words & side_traits)


def _other_side(connector: Connector, room_id: str):
    for side in connector.sides:
        if side.room != room_id:
            return side

    return None


def _connector_blocks_movement(entity: Entity) -> bool:
    openable = entity.components.get(Openable.id)

    return (
        isinstance(openable, Openable)
        and openable.state == OpenState.CLOSED
    )