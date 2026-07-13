from helpers import item, item_with_trait, player, room, statue
import tt
from twip.behavior import Container, Takeable
from twip.world import World


def test_room_adds_named_structural_room_with_trait():
    world = World()

    entity = room(world, tt.ROOM_1)

    assert entity.id in world.entities
    assert entity.names == (tt.ROOM,)
    assert entity.traits == {tt.ROOM_1}
    assert world.can_parent(entity)
    assert not entity.has_behavior(Container.kind)


def test_player_adds_named_entity_without_container_behavior():
    world = World()

    entity = player(world)

    assert entity.id in world.entities
    assert entity.names == (tt.PLAYER,)
    assert entity.traits == set()
    assert not entity.has_behavior(Container.kind)


def test_player_does_not_set_world_player_id():
    world = World()

    entity = player(world)

    assert entity.id in world.entities
    assert world.player_id is None


def test_item_adds_named_takeable():
    world = World()

    entity = item(world, tt.COIN)

    assert entity.id in world.entities
    assert entity.names == (tt.COIN,)
    assert entity.traits == set()
    assert Takeable.kind in entity.behaviors
    assert entity.parent is None


def test_item_with_trait_adds_named_takeable_with_trait():
    world = World()

    entity = item_with_trait(
        world,
        tt.COIN,
        tt.TREASURE,
    )

    assert entity.id in world.entities
    assert entity.names == (tt.COIN,)
    assert entity.traits == {tt.TREASURE}
    assert Takeable.kind in entity.behaviors
    assert entity.parent is None


def test_statue_adds_named_entity_without_behaviors():
    world = World()

    entity = statue(world)

    assert entity.id in world.entities
    assert entity.names == (tt.STATUE,)
    assert entity.traits == set()
    assert entity.behaviors == {}
    assert entity.parent is None