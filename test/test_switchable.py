import tt

from twip.behavior import Switchable, SwitchState
from twip.result import Result
from twip.world import World


def add_switchable(
    world: World,
    *,
    state: SwitchState = SwitchState.OFF,
):
    return world.add(
        names=(tt.THING,),
        behaviors=(
            Switchable(state=state),
        ),
    )


def test_turn_on_switchable_succeeds():
    world = World()
    entity = add_switchable(world)

    result = world.handle("turn on thing")

    assert result == Result.success("You turn on the thing.")
    assert entity.behavior(Switchable.kind).state == SwitchState.ON


def test_turn_switchable_on_succeeds():
    world = World()
    entity = add_switchable(world)

    result = world.handle("turn thing on")

    assert result == Result.success("You turn on the thing.")
    assert entity.behavior(Switchable.kind).state == SwitchState.ON


def test_switch_on_switchable_succeeds():
    world = World()
    entity = add_switchable(world)

    result = world.handle("switch thing on")

    assert result == Result.success("You turn on the thing.")
    assert entity.behavior(Switchable.kind).state == SwitchState.ON


def test_turn_off_switchable_succeeds():
    world = World()
    entity = add_switchable(
        world,
        state=SwitchState.ON,
    )

    result = world.handle("turn off thing")

    assert result == Result.success("You turn off the thing.")
    assert entity.behavior(Switchable.kind).state == SwitchState.OFF


def test_switch_off_switchable_succeeds():
    world = World()
    entity = add_switchable(
        world,
        state=SwitchState.ON,
    )

    result = world.handle("switch thing off")

    assert result == Result.success("You turn off the thing.")
    assert entity.behavior(Switchable.kind).state == SwitchState.OFF


def test_turn_on_already_on_switchable_succeeds():
    world = World()
    entity = add_switchable(
        world,
        state=SwitchState.ON,
    )

    result = world.handle("turn thing on")

    assert result == Result.success("The thing is already on.")
    assert entity.behavior(Switchable.kind).state == SwitchState.ON


def test_turn_off_already_off_switchable_succeeds():
    world = World()
    entity = add_switchable(
        world,
        state=SwitchState.OFF,
    )

    result = world.handle("turn thing off")

    assert result == Result.success("The thing is already off.")
    assert entity.behavior(Switchable.kind).state == SwitchState.OFF


def test_plain_turn_is_not_claimed_by_switchable():
    world = World()
    entity = add_switchable(world)

    result = world.handle("turn thing")

    assert result == Result.failure("You can't do that.")
    assert entity.behavior(Switchable.kind).state == SwitchState.OFF