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


def test_open_closed_wooden_door():
    world = make_world_with_wooden_door()

    result = world.handle("open door")

    door = world.entity("door_wooden").component("openable")

    assert result.ok
    assert result.message == "You open the wooden door."
    assert door.state == OpenState.OPEN
    assert door.is_open


def test_open_already_open_wooden_door():
    world = make_world_with_wooden_door(state=OpenState.OPEN)

    result = world.handle("open door")

    door = world.entity("door_wooden").component("openable")

    assert result.ok
    assert result.message == "The wooden door is already open."
    assert door.state == OpenState.OPEN
    assert door.is_open


def test_open_the_door():
    world = make_world_with_wooden_door()

    result = world.handle("open the door")

    door = world.entity("door_wooden").component("openable")

    assert result.ok
    assert door.state == OpenState.OPEN
    assert door.is_open
    
def test_open_door_by_alias():
    world = World()
    world.add(door_wooden())

    result = world.handle("open door")

    assert result.ok
    assert world.find("door_wooden").component("openable").state == OpenState.OPEN
    
def test_open_unknown_target_fails_cleanly():
    world = World()
    world.add(door_wooden())

    result = world.handle("open window")

    assert not result.ok
    assert "window" in result.message
    
