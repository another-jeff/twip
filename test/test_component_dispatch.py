from typing import ClassVar

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.extension import Containable, Container, Lookable, Openable
from twip.result import Result
from twip.world import World


class BlockingComponent(Component):
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


class LaterComponent(Component):
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


def test_component_that_does_not_claim_action_allows_later_component_to_handle():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    box = world.add(
        names=("box",),
        traits=set(),
        components=(
            Lookable("A plain wooden box."),
            Openable(),
            Containable(),
        ),
    )

    room.components["container"].items.add(box.id)
    box.components["containable"].parent = room.id
    world.current = room.id

    result = world.handle("open box")

    assert result.ok


def test_claimed_failure_stops_component_dispatch():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    switch = world.add(
        names=("switch",),
        traits=set(),
        components=(
            BlockingComponent(),
            LaterComponent(),
            Containable(),
        ),
    )

    room.components["container"].items.add(switch.id)
    switch.components["containable"].parent = room.id
    world.current = room.id

    result = world.handle("poke switch")

    assert not result.ok
    assert result.message == "Blocked."