import tt

from twip import direction
from twip.world import World


def test_world_find_all_includes_connector_touching_current_room():
    world = World()

    room_1 = world.add(names=(tt.ROOM,), traits={tt.ROOM_1})
    room_2 = world.add(names=(tt.ROOM,), traits={tt.ROOM_2})

    door = world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=(
            (room_1, direction.N),
            (room_2, direction.S),
        ),
    )

    world.current = room_1.id

    matches = world.find_all("door")

    assert matches == [door]


def test_world_find_all_uses_current_side_traits():
    world = World()

    room_1 = world.add(names=(tt.ROOM,), traits={tt.ROOM_1})
    room_2 = world.add(names=(tt.ROOM,), traits={tt.ROOM_2})

    door = world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=(
            (room_1, direction.N),
            (room_2, direction.S),
        ),
    )

    world.current = room_1.id

    matches = world.find_all("north door")

    assert matches == [door]


def test_world_find_all_does_not_use_other_side_traits():
    world = World()

    room_1 = world.add(names=(tt.ROOM,), traits={tt.ROOM_1})
    room_2 = world.add(names=(tt.ROOM,), traits={tt.ROOM_2})

    world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=(
            (room_1, direction.N),
            (room_2, direction.S),
        ),
    )

    world.current = room_1.id

    matches = world.find_all("south door")

    assert matches == []


def test_world_find_all_uses_other_side_traits_after_current_room_changes():
    world = World()

    room_1 = world.add(names=(tt.ROOM,), traits={tt.ROOM_1})
    room_2 = world.add(names=(tt.ROOM,), traits={tt.ROOM_2})

    door = world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=(
            (room_1, direction.N),
            (room_2, direction.S),
        ),
    )

    world.current = room_2.id

    matches = world.find_all("south door")

    assert matches == [door]


def test_world_find_all_does_not_include_connector_not_touching_current_room():
    world = World()

    room_1 = world.add(names=(tt.ROOM,), traits={tt.ROOM_1})
    room_2 = world.add(names=(tt.ROOM,), traits={tt.ROOM_2})
    room_3 = world.add(names=(tt.ROOM,), traits={tt.ROOM_3})

    door = world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=(
            (room_2, direction.N),
            (room_3, direction.S),
        ),
    )

    world.current = room_1.id

    matches = world.find_all("door")

    assert door not in matches
    assert matches == []