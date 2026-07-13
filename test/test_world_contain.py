from assertions import assert_contains, assert_does_not_contain
from helpers import coin, statue
from scenario import bs


def test_contain_moves_entity_between_containers():
    s = bs().two_rooms()
    coin_entity = s.put_room(s.room_one, coin)

    s.world.contain(s.room_two, coin_entity)

    assert_does_not_contain(s.room_one, coin_entity)
    assert_contains(s.room_two, coin_entity)
    assert coin_entity.parent == s.room_two.id


def test_contain_in_same_container_is_idempotent():
    s = bs().one_room()
    coin_entity = s.put_room(s.room_one, coin)

    s.world.contain(s.room_one, coin_entity)

    assert_contains(s.room_one, coin_entity)
    assert coin_entity.parent == s.room_one.id


def test_any_entity_can_be_contained_without_a_behavior():
    s = bs().one_room()
    statue_entity = statue(s.world)

    s.world.contain(s.room_one, statue_entity)

    assert_contains(s.room_one, statue_entity)
    assert statue_entity.parent == s.room_one.id