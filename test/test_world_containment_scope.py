from twip.world import World
from twip.behavior import (
    Containable,
    Container,
    Openable,
    OpenState,
)

from helpers import item, room
import tt


def test_current_room_contents_are_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    coin = item(world, tt.COIN)

    world.contain(room_1, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is coin


def test_other_room_contents_are_not_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    coin = item(world, tt.COIN)

    world.contain(room_2, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is None


def test_same_named_entities_in_other_rooms_do_not_create_ambiguity():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    coin_here = item(world, tt.COIN)
    coin_there = item(world, tt.COIN)

    world.contain(room_1, coin_here)
    world.contain(room_2, coin_there)
    world.current = room_1.id

    assert world.find(tt.COIN) is coin_here
    
def test_closed_container_contents_are_not_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Containable(),
            Container(),
            Openable(),
        ),
    )

    coin = item(world, tt.COIN)

    world.contain(room_1, box)
    world.contain(box, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is None


def test_open_container_contents_are_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Containable(),
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )

    coin = item(world, tt.COIN)

    world.contain(room_1, box)
    world.contain(box, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is coin
    
def test_open_container_contents_are_reachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Containable(),
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )

    coin = item(world, tt.COIN)

    world.contain(room_1, box)
    world.contain(box, coin)
    world.current = room_1.id

    assert world.find_reachable_all(tt.COIN) == [coin]
    
def test_closed_container_contents_are_not_reachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Containable(),
            Container(),
            Openable(),
        ),
    )

    coin = item(world, tt.COIN)

    world.contain(room_1, box)
    world.contain(box, coin)
    world.current = room_1.id

    assert world.find_reachable_all(tt.COIN) == []