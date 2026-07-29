from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, ClassVar

from twip.behavior.base import Behavior
from twip.result import Result

if TYPE_CHECKING:
    from twip.action import Action
    from twip.entity import Entity
    from twip.world import World


class WearState(StrEnum):
    NOT_WORN = "not_worn"
    WORN = "worn"


@dataclass
class Wearable(Behavior):
    kind: ClassVar[str] = "wearable"

    state: WearState = WearState.NOT_WORN

def handle(
    self,
    action: Action,
    entity: Entity,
    world: World,
) -> Result | None:
    if action.verb == "wear":
        return self._wear(entity, world)

    if action.verb == "remove":
        return self._remove(entity, world)

    return None

def _wear(
    self,
    entity: Entity,
    world: World,
) -> Result | None:
    if entity.parent != world.player_id:
        return None

    if self.state == WearState.WORN:
        return Result.success(
            world.language.already_wearing(entity)
        )

    self.state = WearState.WORN

    return Result.success(
        world.language.wear_success(entity),
        consumes_turn=True,
    )

def _remove(
    self,
    entity: Entity,
    world: World,
) -> Result | None:
    if entity.parent != world.player_id:
        return None

    if self.state != WearState.WORN:
        return None

    self.state = WearState.NOT_WORN

    return Result.success(
        world.language.remove_success(entity),
        consumes_turn=True,
    )