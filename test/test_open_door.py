from twip import World
from twip.preset import make_door_wooden


def make_world_with_wooden_door(*, is_open: bool = False) -> World:
    world = World()
    world.add_entity(make_door_wooden(is_open=is_open))
    return world


def test_open_closed_wooden_door():
    world = make_world_with_wooden_door()

    result = world.handle("open door")

    assert result.succeeded
    assert result.message == "You open the wooden door."
    assert world.entity("door_wooden").component("door").is_open


def test_open_already_open_wooden_door():
    world = make_world_with_wooden_door(is_open=True)

    result = world.handle("open door")

    assert result.succeeded
    assert result.message == "The wooden door is already open."
    assert world.entity("door_wooden").component("door").is_open


def test_open_the_door():
    world = make_world_with_wooden_door()

    result = world.handle("open the door")

    assert result.succeeded
    assert world.entity("door_wooden").component("door").is_open