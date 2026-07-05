# test/test_world_containment_scope.py

from twip.extension import Containable, Container
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