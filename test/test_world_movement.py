# test/test_world_movement.py

from twip import dir
from twip.extension import Container, Containable, Lockable, LockState, Openable, OpenState
from twip.world import World

import tt


def room(world: World, trait: str):
    return world.add(
        names=(tt.ROOM,),
        traits={trait},
        components=(Container(),),
    )
    
def item(world: World, name: str):
    return world.add(
        names=(name,),
        traits=set(),
        components=(Containable(),),
    )


def test_go_direction_moves_to_connected_room():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
    )

    world.current = room_1.id

    result = world.handle("go north")

    assert result.ok
    assert world.current == room_2.id


def test_go_unknown_direction_fails_cleanly():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    world.current = room_1.id

    result = world.handle("go north")

    assert not result.ok
    assert world.current == room_1.id
    
    
def test_go_direction_through_closed_door_fails_cleanly():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
        components=(Openable(state=OpenState.CLOSED),),
    )

    world.current = room_1.id

    result = world.handle("go north")

    assert not result.ok
    assert world.current == room_1.id
    
    
def test_go_direction_through_open_door_moves_to_connected_room():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
        components=(Openable(state=OpenState.OPEN),),
    )

    world.current = room_1.id

    result = world.handle("go north")

    assert result.ok
    assert world.current == room_2.id
    
    
def test_movement_changes_visible_room_contents():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    coin = item(world, tt.COIN)
    gem = item(world, tt.GEM)

    world.contain(room_1, coin)
    world.contain(room_2, gem)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
    )

    world.current = room_1.id

    assert world.find(tt.COIN) is coin
    assert world.find(tt.GEM) is None

    result = world.handle("go north")

    assert result.ok
    assert world.current == room_2.id
    assert world.find(tt.COIN) is None
    assert world.find(tt.GEM) is gem
    
    
def test_go_ambiguous_direction_fails_without_moving():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)
    room_3 = room(world, tt.ROOM_3)

    world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=((room_1, dir.N), (room_2, dir.S)),
    )

    world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.STONE},
        connections=((room_1, dir.N), (room_3, dir.S)),
    )

    world.current = room_1.id

    result = world.handle("go north")

    assert not result.ok
    assert world.current == room_1.id
    
    
def test_go_direction_with_connector_traits_resolves_ambiguous_exit():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)
    room_3 = room(world, tt.ROOM_3)

    world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=((room_1, dir.N), (room_2, dir.S)),
    )

    world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.STONE},
        connections=((room_1, dir.N), (room_3, dir.S)),
    )

    world.current = room_1.id

    result = world.handle("go north wooden door")

    assert result.ok
    assert world.current == room_2.id
    
    
def test_go_direction_with_connector_traits_through_closed_door_fails():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        traits={tt.WOODEN},
        connections=((room_1, dir.N), (room_2, dir.S)),
        components=(Openable(state=OpenState.CLOSED),),
    )

    world.current = room_1.id

    result = world.handle("go north wooden door")

    assert not result.ok
    assert world.current == room_1.id
    
    
def test_open_door_then_go_direction_moves_to_connected_room():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
        components=(Openable(state=OpenState.CLOSED),),
    )

    world.current = room_1.id

    go_closed = world.handle("go north")

    assert not go_closed.ok
    assert world.current == room_1.id

    opened = world.handle("open north door")

    assert opened.ok

    go_open = world.handle("go north")

    assert go_open.ok
    assert world.current == room_2.id
    
    
def test_movement_uses_other_side_direction_after_room_changes():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
    )

    world.current = room_1.id

    north = world.handle("go north")

    assert north.ok
    assert world.current == room_2.id

    wrong_way = world.handle("go north")

    assert not wrong_way.ok
    assert world.current == room_2.id

    south = world.handle("go south")

    assert south.ok
    assert world.current == room_1.id


def test_locked_closed_door_cannot_be_opened_or_moved_through():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
        components=(
            Openable(state=OpenState.CLOSED),
            Lockable(state=LockState.LOCKED),
        ),
    )

    world.current = room_1.id

    opened = world.handle("open north door")

    assert not opened.ok
    assert world.current == room_1.id

    moved = world.handle("go north")

    assert not moved.ok
    assert world.current == room_1.id
    
    
def test_unlock_open_then_go_moves_through_door():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    world.add_and_connect(
        names=(tt.DOOR,),
        connections=((room_1, dir.N), (room_2, dir.S)),
        components=(
            Openable(state=OpenState.CLOSED),
            Lockable(state=LockState.LOCKED),
        ),
    )

    world.current = room_1.id

    unlocked = world.handle("unlock north door")

    assert unlocked.ok

    opened = world.handle("open north door")

    assert opened.ok

    moved = world.handle("go north")

    assert moved.ok
    assert world.current == room_2.id