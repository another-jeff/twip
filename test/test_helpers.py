from helpers import item, item_with_trait, player, room, statue

import tt

from twip.extension import Containable, Container
from twip.world import World


def test_room_adds_named_container_with_trait():
    world = World()

    entity = room(world, tt.ROOM_1)

    assert entity.id in world.entities
    assert entity.names == (tt.ROOM,)
    assert entity.traits == {tt.ROOM_1}
    assert Container.id in entity.components


def test_player_adds_named_container():
    world = World()

    entity = player(world)

    assert entity.id in world.entities
    assert entity.names == (tt.PLAYER,)
    assert entity.traits == set()
    assert Container.id in entity.components


def test_player_does_not_set_world_player_id():
    world = World()

    entity = player(world)

    assert entity.id in world.entities
    assert world.player_id is None


def test_item_adds_named_containable():
    world = World()

    entity = item(world, tt.COIN)

    assert entity.id in world.entities
    assert entity.names == (tt.COIN,)
    assert entity.traits == set()
    assert Containable.id in entity.components


def test_item_with_trait_adds_named_containable_with_trait():
    world = World()

    entity = item_with_trait(world, tt.COIN, tt.TREASURE)

    assert entity.id in world.entities
    assert entity.names == (tt.COIN,)
    assert entity.traits == {tt.TREASURE}
    assert Containable.id in entity.components


def test_statue_adds_named_entity_without_components():
    world = World()

    entity = statue(world)

    assert entity.id in world.entities
    assert entity.names == (tt.STATUE,)
    assert entity.traits == set()
    assert entity.components == {}