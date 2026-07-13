from twip.behavior import Container
from twip.world import World

from assertions import assert_contains, assert_does_not_contain
from helpers import coin, coin_blue, coin_red, player
from scenario import bs

import tt


def test_drop_disambiguated_inventory_item_moves_only_that_item():
    s = bs().one_room().with_player()

    red = s.put_inventory(coin_red)
    blue = s.put_inventory(coin_blue)

    result = s.handle("drop red coin")

    assert result.ok

    assert_does_not_contain(s.player, red)
    assert_contains(s.room_one, red)

    assert_contains(s.player, blue)
    assert_does_not_contain(s.room_one, blue)


def test_drop_inventory_item_moves_it_to_current_room():
    s = bs().one_room().with_player()

    inventory_item = s.put_inventory(coin)

    result = s.handle("drop coin")

    assert result.ok
    assert_does_not_contain(s.player, inventory_item)
    assert_contains(s.room_one, inventory_item)


def test_drop_visible_room_item_not_in_inventory_fails_without_mutation():
    s = bs().one_room().with_player()

    room_item = s.put_room(s.room_one, coin)

    result = s.handle("drop coin")

    assert not result.ok
    assert_contains(s.room_one, room_item)
    assert_does_not_contain(s.player, room_item)


def test_take_ambiguous_visible_items_fails_without_mutation():
    s = bs().one_room().with_player()

    first_coin = s.put_room(s.room_one, coin)
    second_coin = s.put_room(s.room_one, coin)

    result = s.handle("take coin")

    assert not result.ok

    assert_contains(s.room_one, first_coin)
    assert_contains(s.room_one, second_coin)

    assert_does_not_contain(s.player, first_coin)
    assert_does_not_contain(s.player, second_coin)


def test_drop_ambiguous_inventory_items_fails_without_mutation():
    s = bs().one_room().with_player()

    first_coin = s.put_inventory(coin)
    second_coin = s.put_inventory(coin)

    result = s.handle("drop coin")

    assert not result.ok

    assert_contains(s.player, first_coin)
    assert_contains(s.player, second_coin)

    assert_does_not_contain(s.room_one, first_coin)
    assert_does_not_contain(s.room_one, second_coin)


def test_drop_same_named_visible_room_item_does_not_create_ambiguity():
    s = bs().one_room().with_player()

    room_coin = s.put_room(s.room_one, coin)
    carried_coin = s.put_inventory(coin)

    result = s.handle("drop coin")

    assert result.ok

    assert_does_not_contain(s.player, carried_coin)
    assert_contains(s.room_one, carried_coin)

    assert_contains(s.room_one, room_coin)
    assert_does_not_contain(s.player, room_coin)


def test_drop_after_room_change_puts_item_in_new_current_room():
    s = bs().two_rooms().with_player()

    coin_entity = s.put_inventory(coin)

    s.world.current = s.room_two.id

    result = s.handle("drop coin")

    assert result.ok

    assert_does_not_contain(s.player, coin_entity)
    assert_does_not_contain(s.room_one, coin_entity)
    assert_contains(s.room_two, coin_entity)
    

def test_drop_does_not_require_player_container_behavior():
    world = World()

    room = world.add_room(names=("room",))
    world.current = room.id

    player_entity = world.add(names=("player",))
    world.player_id = player_entity.id

    coin_entity = coin(world)
    world.put(player_entity, coin_entity)

    result = world.handle("drop coin")

    assert result.ok
    assert not player_entity.has_behavior(Container.kind)
    assert world.contents_of(player_entity) == []
    assert world.contents_of(room) == [coin_entity]
    assert coin_entity.parent == room.id