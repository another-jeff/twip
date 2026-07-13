import pytest

from twip.behavior import Container
from twip.world import World

from assertions import assert_contains, assert_does_not_contain
from helpers import coin, statue
from scenario import bs


def test_contain_moves_entity_between_containers():
    s = bs().two_rooms()

    coin_entity = s.put_room(s.room_one, coin)

    s.world.put(s.room_two, coin_entity)

    assert_does_not_contain(s.room_one, coin_entity)
    assert_contains(s.room_two, coin_entity)
    assert coin_entity.parent == s.room_two.id


def test_contain_in_same_container_is_idempotent():
    s = bs().one_room()

    coin_entity = s.put_room(s.room_one, coin)

    s.world.put(s.room_one, coin_entity)

    assert_contains(s.room_one, coin_entity)
    assert coin_entity.parent == s.room_one.id


def test_any_entity_can_be_contained_without_a_behavior():
    s = bs().one_room()

    statue_entity = statue(s.world)

    s.world.put(s.room_one, statue_entity)

    assert_contains(s.room_one, statue_entity)
    assert statue_entity.parent == s.room_one.id


def test_room_can_parent_without_container_behavior():
    world = World()

    room = world.add_room(names=("room",))
    coin_entity = coin(world)

    world.put(room, coin_entity)

    assert not room.has_behavior(Container.kind)
    assert world.contents_of(room) == [coin_entity]
    assert coin_entity.parent == room.id


def test_player_can_parent_without_container_behavior():
    world = World()

    player = world.add(names=("player",))
    world.player_id = player.id
    coin_entity = coin(world)

    world.put(player, coin_entity)

    assert not player.has_behavior(Container.kind)
    assert world.contents_of(player) == [coin_entity]
    assert coin_entity.parent == player.id


def test_container_behavior_allows_ordinary_entity_to_parent():
    world = World()

    box = world.add(
        names=("box",),
        behaviors=(Container(),),
    )
    coin_entity = coin(world)

    world.put(box, coin_entity)

    assert world.contents_of(box) == [coin_entity]
    assert coin_entity.parent == box.id


def test_ordinary_entity_cannot_parent():
    world = World()

    desk = world.add(names=("desk",))
    coin_entity = coin(world)

    with pytest.raises(ValueError, match="cannot contain"):
        world.put(desk, coin_entity)

    assert coin_entity.parent is None


def test_entity_cannot_contain_itself():
    world = World()

    box = world.add(
        names=("box",),
        behaviors=(Container(),),
    )

    with pytest.raises(ValueError, match="itself"):
        world.put(box, box)

    assert box.parent is None
    assert world.contents_of(box) == []


def test_containment_cycle_is_rejected_without_mutation():
    world = World()

    outer_box = world.add(
        names=("outer box",),
        behaviors=(Container(),),
    )
    inner_box = world.add(
        names=("inner box",),
        behaviors=(Container(),),
    )

    world.put(outer_box, inner_box)

    with pytest.raises(ValueError, match="cycle"):
        world.put(inner_box, outer_box)

    assert outer_box.parent is None
    assert inner_box.parent == outer_box.id
    assert world.contents_of(outer_box) == [inner_box]
    assert world.contents_of(inner_box) == []