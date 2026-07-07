import tt

from twip import direction
from twip.behavior.openable import Openable, OpenState
from twip.world import World


def test_open_door_is_ambiguous_when_multiple_doors_visible():
    world, north_door, south_door = _world_with_two_visible_doors()

    result = world.handle("open door")

    assert not result.ok
    assert north_door.behavior(Openable.kind).state == OpenState.CLOSED
    assert south_door.behavior(Openable.kind).state == OpenState.CLOSED


def test_open_north_door_opens_only_north_door():
    world, north_door, south_door = _world_with_two_visible_doors()

    result = world.handle("open north door")

    assert result.ok
    assert north_door.behavior(Openable.kind).state == OpenState.OPEN
    assert south_door.behavior(Openable.kind).state == OpenState.CLOSED


def _world_with_two_visible_doors():
    world = World()

    room_1 = world.add(names=(tt.ROOM,), traits={tt.ROOM_1})
    room_2 = world.add(names=(tt.ROOM,), traits={tt.ROOM_2})
    room_3 = world.add(names=(tt.ROOM,), traits={tt.ROOM_3})

    north_door = world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        behaviors=(Openable(),),
        connections=(
            (room_1, direction.N),
            (room_2, direction.S),
        ),
    )

    south_door = world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        behaviors=(Openable(),),
        connections=(
            (room_1, direction.S),
            (room_3, direction.N),
        ),
    )

    world.current = room_1.id

    return world, north_door, south_door