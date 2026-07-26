from __future__ import annotations

from typing import TYPE_CHECKING

from twip.result import Result

if TYPE_CHECKING:
    from twip.action import Action
    from twip.world import World


def handle(world: World, action: Action) -> Result:
    return Result.success(
        world.language.wait_success(),
        consumes_turn=True,
    )