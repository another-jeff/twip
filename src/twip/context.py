from __future__ import annotations

from typing import TYPE_CHECKING

from twip.entity import Entity
from twip.result import Result

if TYPE_CHECKING:
    from twip.world import World


type PlayerRoom = tuple[Entity, Entity]


def require_player(world: World) -> Entity | Result:
    if not world.player_id:
        return Result.failure(world.language.missing_player())

    player = world.entities.get(world.player_id)

    if player is None:
        return Result.failure(world.language.missing_player())

    return player


def require_current_room(world: World) -> Entity | Result:
    if not world.current:
        return Result.failure(world.language.missing_current_room())

    room = world.entities.get(world.current)

    if room is None:
        return Result.failure(world.language.missing_current_room())

    return room


def require_player_room(world: World) -> PlayerRoom | Result:
    player = require_player(world)

    if isinstance(player, Result):
        return player

    room = require_current_room(world)

    if isinstance(room, Result):
        return room

    return player, room