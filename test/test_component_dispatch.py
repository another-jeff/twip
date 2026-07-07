from typing import ClassVar

from twip.action import Action
from twip.behavior import Behavior
from twip.entity import Entity
from twip.behavior import Containable, Container, Lookable, Openable
from twip.result import Result
from twip.world import World


class BlockingBehavior(Behavior):
    kind: ClassVar[str] = "blocking"

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: object,
    ) -> Result | None:
        if action.verb == "poke":
            return Result.failure("Blocked.")

        return None


class LaterBehavior(Behavior):
    kind: ClassVar[str] = "later"

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: object,
    ) -> Result | None:
        if action.verb == "poke":
            return Result.success("Handled later.")

        return None


def test_behavior_that_does_not_claim_action_allows_later_behavior_to_handle():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        behaviors=(Container(),),
    )

    box = world.add(
        names=("box",),
        traits=set(),
        behaviors=(
            Lookable("A plain wooden box."),
            Openable(),
            Containable(),
        ),
    )

    room.behaviors["container"].items.add(box.id)
    box.behaviors["containable"].parent = room.id
    world.current = room.id

    result = world.handle("open box")

    assert result.ok


def test_claimed_failure_stops_behavior_dispatch():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        behaviors=(Container(),),
    )

    switch = world.add(
        names=("switch",),
        traits=set(),
        behaviors=(
            BlockingBehavior(),
            LaterBehavior(),
            Containable(),
        ),
    )

    room.behaviors["container"].items.add(switch.id)
    switch.behaviors["containable"].parent = room.id
    world.current = room.id

    result = world.handle("poke switch")

    assert not result.ok
    assert result.message == "Blocked."