from twip.world import World
from twip.behavior import (
    Container,
    Openable,
    OpenState,
)

from helpers import item, player, room
import tt


def test_current_room_contents_are_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    coin = item(world, tt.COIN)

    world.put(room_1, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is coin


def test_other_room_contents_are_not_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    coin = item(world, tt.COIN)

    world.put(room_2, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is None


def test_same_named_entities_in_other_rooms_do_not_create_ambiguity():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    room_2 = room(world, tt.ROOM_2)

    coin_here = item(world, tt.COIN)
    coin_there = item(world, tt.COIN)

    world.put(room_1, coin_here)
    world.put(room_2, coin_there)
    world.current = room_1.id

    assert world.find(tt.COIN) is coin_here
    
def test_closed_container_contents_are_not_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Container(),
            Openable(),
        ),
    )

    coin = item(world, tt.COIN)

    world.put(room_1, box)
    world.put(box, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is None


def test_open_container_contents_are_visible():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )

    coin = item(world, tt.COIN)

    world.put(room_1, box)
    world.put(box, coin)
    world.current = room_1.id

    assert world.find(tt.COIN) is coin
    
def test_open_container_contents_are_reachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )

    coin = item(world, tt.COIN)

    world.put(room_1, box)
    world.put(box, coin)
    world.current = room_1.id

    assert world.find_reachable_all(tt.COIN) == [coin]
    
def test_closed_container_contents_are_not_reachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)

    box = world.add(
        names=("box",),
        behaviors=(
            Container(),
            Openable(),
        ),
    )

    coin = item(world, tt.COIN)

    world.put(room_1, box)
    world.put(box, coin)
    world.current = room_1.id

    assert world.find_reachable_all(tt.COIN) == []
    
    
def test_player_inventory_is_visible_and_reachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    player_entity = player(world)
    coin = item(world, tt.COIN)

    world.current = room_1.id
    world.player_id = player_entity.id
    world.put(player_entity, coin)

    assert world.find(tt.COIN) is coin
    assert world.find_reachable_all(tt.COIN) == [coin]


def test_open_carried_container_contents_are_visible_and_reachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    player_entity = player(world)
    box = world.add(
        names=("box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    coin = item(world, tt.COIN)

    world.current = room_1.id
    world.player_id = player_entity.id
    world.put(player_entity, box)
    world.put(box, coin)

    assert world.find(tt.COIN) is coin
    assert world.find_reachable_all(tt.COIN) == [coin]


def test_closed_carried_container_contents_are_hidden_and_unreachable():
    world = World()

    room_1 = room(world, tt.ROOM_1)
    player_entity = player(world)
    box = world.add(
        names=("box",),
        behaviors=(
            Container(),
            Openable(),
        ),
    )
    coin = item(world, tt.COIN)

    world.current = room_1.id
    world.player_id = player_entity.id
    world.put(player_entity, box)
    world.put(box, coin)

    assert world.find(tt.COIN) is None
    assert world.find_reachable_all(tt.COIN) == []