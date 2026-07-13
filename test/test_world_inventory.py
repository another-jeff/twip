from assertions import assert_ok_contains, assert_ok_omits
from helpers import item
from scenario import bs
from twip.behavior import Container
from twip.world import World

import tt


def test_inventory_lists_only_carried_items_not_room_items():
    s = bs().one_room().with_player()

    carried_key = item(s.world, tt.KEY)
    room_coin = item(s.world, tt.COIN)

    s.world.put(s.player, carried_key)
    s.world.put(s.room_one, room_coin)

    result = s.handle("inventory")

    assert_ok_contains(result, tt.KEY)
    assert_ok_omits(result, tt.COIN)


def test_inventory_lists_multiple_carried_items():
    s = bs().with_player()

    coin_entity = item(s.world, tt.COIN)
    key_entity = item(s.world, tt.KEY)

    s.world.put(s.player, coin_entity)
    s.world.put(s.player, key_entity)

    result = s.handle("inventory")

    assert_ok_contains(result, tt.COIN)
    assert_ok_contains(result, tt.KEY)


def test_inventory_lists_carried_item():
    s = bs().with_player()

    coin_entity = item(s.world, tt.COIN)
    s.world.put(s.player, coin_entity)

    result = s.handle("inventory")

    assert_ok_contains(result, tt.COIN)


def test_inventory_empty_reports_nothing_carried():
    s = bs().with_player()

    result = s.handle("inventory")

    assert_ok_contains(result, "nothing")


def test_inventory_without_player_fails():
    s = bs()

    result = s.handle("inventory")

    assert not result.ok
    assert tt.PLAYER in result.message


def test_empty_inventory_does_not_require_container_behavior():
    world = World()

    player = world.add(names=(tt.PLAYER,))
    world.player_id = player.id

    result = world.handle("inventory")

    assert_ok_contains(result, "nothing")
    assert not player.has_behavior(Container.kind)


def test_inventory_uses_structural_contents():
    world = World()

    player = world.add(names=(tt.PLAYER,))
    world.player_id = player.id

    coin_entity = item(world, tt.COIN)
    world.put(player, coin_entity)

    result = world.handle("inventory")

    assert_ok_contains(result, tt.COIN)
    assert not player.has_behavior(Container.kind)