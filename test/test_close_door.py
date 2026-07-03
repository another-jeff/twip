from twip import World
from twip.extension import OpenState
from twip.preset import door_wooden


def make_world_with_wooden_door(
    *,
    state: OpenState = OpenState.CLOSED,
) -> World:
    world = World()
    world.add(door_wooden(state=state))
    return world


def test_close_open_wooden_door():
    world = make_world_with_wooden_door(state=OpenState.OPEN)

    result = world.handle("close door")

    door = world.entity("door_wooden").component("openable")

    assert result.ok
    assert result.message == "You close the wooden door."
    assert door.state == OpenState.CLOSED
    assert door.is_closed


def test_close_already_closed_wooden_door():
    world = make_world_with_wooden_door()

    result = world.handle("close door")

    door = world.entity("door_wooden").component("openable")

    assert result.ok
    assert result.message == "The wooden door is already closed."
    assert door.state == OpenState.CLOSED
    assert door.is_closed


def test_close_the_door():
    world = make_world_with_wooden_door(state=OpenState.OPEN)

    result = world.handle("close the door")

    door = world.entity("door_wooden").component("openable")

    assert result.ok
    assert door.state == OpenState.CLOSED
    assert door.is_closed