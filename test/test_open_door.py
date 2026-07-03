from twip import World
from twip.extension import DoorState
from twip.preset import make_door_wooden


def make_world_with_wooden_door(
    *,
    state: DoorState = DoorState.CLOSED,
) -> World:
    world = World()
    world.add_entity(make_door_wooden(state=state))
    return world


def test_open_closed_wooden_door():
    world = make_world_with_wooden_door()

    result = world.handle("open door")

    door = world.entity("door_wooden").component("door")

    assert result.succeeded
    assert result.message == "You open the wooden door."
    assert door.state == DoorState.OPEN
    assert door.is_open


def test_open_already_open_wooden_door():
    world = make_world_with_wooden_door(state=DoorState.OPEN)

    result = world.handle("open door")

    door = world.entity("door_wooden").component("door")

    assert result.succeeded
    assert result.message == "The wooden door is already open."
    assert door.state == DoorState.OPEN
    assert door.is_open


def test_open_the_door():
    world = make_world_with_wooden_door()

    result = world.handle("open the door")

    door = world.entity("door_wooden").component("door")

    assert result.succeeded
    assert door.state == DoorState.OPEN
    assert door.is_open