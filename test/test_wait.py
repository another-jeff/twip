from twip.result import Result
from twip.world import World


def test_wait_consumes_one_turn():
    world = World()

    result = world.handle("wait")

    assert result == Result.success(
        "Time passes.",
        consumes_turn=True,
    )
    assert world.turn == 1


def test_z_waits_and_consumes_one_turn():
    world = World()

    result = world.handle("z")

    assert result == Result.success(
        "Time passes.",
        consumes_turn=True,
    )
    assert world.turn == 1


def test_non_turn_action_does_not_advance_turn():
    world = World()

    world.handle("inventory")

    assert world.turn == 0


def test_multiple_waits_advance_monotonically():
    world = World()

    world.handle("wait")
    world.handle("wait")
    world.handle("z")

    assert world.turn == 3