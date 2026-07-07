from typing import ClassVar

from twip.action import Action
from twip.behavior import Behavior, Containable
from twip.entity import Entity
from twip.result import Result
from twip.world import World

from assertions import assert_ok_message
from scenario import bs


SWITCH = "switch"


class IgnoringBehavior(Behavior):
    kind: ClassVar[str] = "ignoring"

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: World,
    ) -> Result | None:
        return None


class BlockingBehavior(Behavior):
    kind: ClassVar[str] = "blocking"

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: World,
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
        world: World,
    ) -> Result | None:
        if action.verb == "poke":
            return Result.success("Handled later.")

        return None
    

class FirstHandlingBehavior(Behavior):
    kind: ClassVar[str] = "first-handling"

    def handle(
        self,
        action: Action,
        entity: Entity,
        world: World,
    ) -> Result | None:
        if action.verb == "poke":
            return Result.success("Handled first.")

        return None


def switch_with(*behaviors: Behavior):
    def factory(world: World):
        return world.add(
            names=(SWITCH,),
            traits=set(),
            behaviors=(
                *behaviors,
                Containable(),
            ),
        )

    return factory


def test_behavior_that_does_not_claim_action_allows_later_behavior_to_handle():
    s = bs().one_room()
    s.put_room(
        s.room_one,
        switch_with(
            IgnoringBehavior(),
            LaterBehavior(),
        ),
    )

    result = s.handle("poke switch")

    assert_ok_message(result, "Handled later.")


def test_claimed_failure_stops_behavior_dispatch():
    s = bs().one_room()
    s.put_room(
        s.room_one,
        switch_with(
            BlockingBehavior(),
            LaterBehavior(),
        ),
    )

    result = s.handle("poke switch")

    assert not result.ok
    assert result.message == "Blocked."
    
    
def test_claimed_success_stops_behavior_dispatch():
    s = bs().one_room()
    s.put_room(
        s.room_one,
        switch_with(
            FirstHandlingBehavior(),
            LaterBehavior(),
        ),
    )

    result = s.handle("poke switch")

    assert_ok_message(result, "Handled first.")