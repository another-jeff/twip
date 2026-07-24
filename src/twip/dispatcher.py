from __future__ import annotations

from typing import TYPE_CHECKING

from twip import direction
from twip.action import Action
from twip.command import (
    drop,
    inventory,
    look,
    move,
    put,
    take,
    wait,
)
from twip.result import Result
from twip.verb import VERBS

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


def dispatch(world: World, action: Action) -> Result:
    match action.verb:
        case None | "":
            return Result.failure("Nothing happens.")

        case "inventory":
            return inventory.handle(world)

        case "look" if not action.target:
            return look.room(world)

        case "wait":
            return wait.handle()

        case _ if not action.target:
            return _handle_targetless_action(world, action)

        case "look":
            return look.target(world, action)

        case "take":
            return take.handle(world, action.target)

        case "drop":
            return drop.handle(world, action.target)

        case "put":
            return put.handle(world, action)

        case "go":
            return move.handle(world, action.target)

        case "move" if direction.is_direction(action.target):
            return move.handle(
                world,
                direction.normalize(action.target),
            )

        case _:
            return _handle_targeted_action(world, action)


def _handle_targeted_action(
    world: World,
    action: Action,
) -> Result:
    target = action.target

    if not target:
        return Result.failure(
            f"{action.verb.capitalize()} what?"
        )

    resolved = _resolve_reachable_target(world, target)

    if isinstance(resolved, Result):
        return resolved

    result = resolved.handle(action, world)

    if result is None:
        return Result.failure("You can't do that.")

    return result


def _handle_targetless_action(
    world: World,
    action: Action,
) -> Result:
    result = _handle_current_room_action(world, action)

    if result is not None:
        return result

    result = _handle_player_action(world, action)

    if result is not None:
        return result

    verb = action.verb or ""

    if _verb_requires_target(verb):
        return Result.failure(f"{verb.capitalize()} what?")

    return Result.failure("Nothing happens.")


def _handle_current_room_action(
    world: World,
    action: Action,
) -> Result | None:
    if world.current is None:
        return None

    entity = world.entities.get(world.current)

    if entity is None:
        return None

    return entity.handle(action, world)


def _handle_player_action(
    world: World,
    action: Action,
) -> Result | None:
    if world.player_id is None:
        return None

    entity = world.entities.get(world.player_id)

    if entity is None:
        return None

    return entity.handle(action, world)


def _verb_requires_target(verb: str) -> bool:
    policy = VERBS.get(verb)

    if policy is None:
        return True

    return policy.requires_target


def _resolve_reachable_target(
    world: World,
    target: str,
) -> Entity | Result:
    matching_entities = world.find_reachable_all(target)

    if not matching_entities:
        return Result.failure(
            world.language.not_seen(target)
        )

    if len(matching_entities) > 1:
        return Result.failure(
            f"Which {target} do you mean?"
        )

    return matching_entities[0]