from twip.behavior import Containable

from assertions import assert_contains, assert_does_not_contain
from helpers import coin
from scenario import bs


def test_contain_moves_entity_between_containers():
    s = bs().two_rooms()
    coin_entity = s.put_room(s.room_one, coin)

    s.world.contain(s.room_two, coin_entity)

    assert_does_not_contain(s.room_one, coin_entity)
    assert_contains(s.room_two, coin_entity)

    containable = coin_entity.behavior(Containable.kind)
    assert containable.parent == s.room_two.id


def test_contain_in_same_container_is_idempotent():
    s = bs().one_room()
    coin_entity = s.put_room(s.room_one, coin)

    s.world.contain(s.room_one, coin_entity)

    assert_contains(s.room_one, coin_entity)

    containable = coin_entity.behavior(Containable.kind)
    assert containable.parent == s.room_one.id