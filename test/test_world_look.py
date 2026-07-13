from twip.behavior import Container
from twip.world import World

from assertions import (
    assert_not_ok_contains,
    assert_not_ok_contains_any,
    assert_ok_contains,
    assert_ok_message,
    assert_ok_omits,
)
from helpers import (
    coin_copper,
    coin_silver,
    item,
)
from scenario import bs

import tt


def item_factory(name: str):
    return lambda world: item(world, name)


def test_look_describes_current_room():
    s = bs().one_room()

    result = s.handle("look")

    assert_ok_contains(result, tt.ROOM_1)


def test_look_without_current_room_fails_cleanly():
    s = bs()

    result = s.handle("look")

    assert_not_ok_contains_any(result, "nowhere", "current")


def test_look_lists_current_room_contents():
    s = bs().one_room()

    s.put_room(s.room_one, item_factory(tt.COIN))

    result = s.handle("look")

    assert_ok_contains(result, tt.ROOM_1, tt.COIN)


def test_look_lists_only_current_room_contents():
    s = bs().two_rooms()

    s.put_room(s.room_one, item_factory(tt.COIN))
    s.put_room(s.room_two, item_factory(tt.GEM))

    result = s.handle("look")

    assert_ok_contains(result, tt.ROOM_1, tt.COIN)
    assert_ok_omits(result, tt.GEM)


def test_look_does_not_list_inventory_contents():
    s = bs().one_room().with_player()

    s.put_inventory(item_factory(tt.COIN))

    result = s.handle("look")

    assert_ok_contains(result, tt.ROOM_1)
    assert_ok_omits(result, tt.COIN)


def test_look_lists_multiple_current_room_contents():
    s = bs().one_room()

    s.put_room(
        s.room_one,
        item_factory(tt.COIN),
        item_factory(tt.KEY),
    )

    result = s.handle("look")

    assert_ok_contains(result, tt.ROOM_1, tt.COIN, tt.KEY)


def test_look_lists_room_contents_in_name_order():
    s = bs().one_room()

    s.put_room(
        s.room_one,
        item_factory(tt.ZEBRA),
        item_factory(tt.APPLE),
    )

    result = s.handle("look")

    assert result.ok
    assert result.message.index(tt.APPLE) < result.message.index(tt.ZEBRA)


def test_look_includes_current_room_lookable_text():
    s = bs().one_room()

    result = s.handle("look")

    assert_ok_contains(result, tt.ROOM_1, tt.ROOM_DESCRIPTION)


def test_look_target_describes_visible_lookable_entity():
    s = bs().one_room()

    s.put_room(s.room_one, coin_copper)

    result = s.handle("look coin")

    assert_ok_message(result, tt.COPPER_COIN_DESCRIPTION)


def test_look_target_ignores_lookable_entity_in_other_room():
    s = bs().two_rooms()

    s.put_room(s.room_two, coin_copper)

    result = s.handle("look coin")

    assert_not_ok_contains(result, tt.COIN)


def test_look_target_ambiguity_fails_cleanly():
    s = bs().one_room()

    s.put_room(s.room_one, coin_copper, coin_silver)

    result = s.handle("look coin")

    assert_not_ok_contains(result, "Which coin")


def test_look_target_disambiguation_describes_selected_entity():
    s = bs().one_room()

    s.put_room(s.room_one, coin_copper, coin_silver)

    result = s.handle("look silver coin")

    assert_ok_message(result, tt.SILVER_COIN_DESCRIPTION)


def test_look_target_visible_non_lookable_fails_cleanly():
    s = bs().one_room()

    s.put_room(s.room_one, item_factory(tt.ROCK))

    result = s.handle("look rock")

    assert_not_ok_contains(result, "can't do that")


def test_look_target_can_describe_inventory_item():
    s = bs().one_room().with_player()

    s.put_inventory(coin_copper)

    result = s.handle("look coin")

    assert_ok_message(result, tt.COPPER_COIN_DESCRIPTION)


def test_look_target_ambiguity_includes_room_and_inventory_items():
    s = bs().one_room().with_player()

    s.put_room(s.room_one, coin_copper)
    s.put_inventory(coin_silver)

    result = s.handle("look coin")

    assert_not_ok_contains(result, "Which coin")


def test_look_target_disambiguation_selects_inventory_item_over_room_item():
    s = bs().one_room().with_player()

    s.put_room(s.room_one, coin_copper)
    s.put_inventory(coin_silver)

    result = s.handle("look silver coin")

    assert_ok_message(result, tt.SILVER_COIN_DESCRIPTION)


def test_look_target_disambiguation_selects_room_item_over_inventory_item():
    s = bs().one_room().with_player()

    s.put_room(s.room_one, coin_copper)
    s.put_inventory(coin_silver)

    result = s.handle("look copper coin")

    assert_ok_message(result, tt.COPPER_COIN_DESCRIPTION)


def test_look_target_inventory_non_lookable_fails_cleanly():
    s = bs().one_room().with_player()

    s.put_inventory(item_factory(tt.ROCK))

    result = s.handle("look rock")

    assert_not_ok_contains(result, "can't do that")


def test_look_target_inventory_item_ignores_same_named_item_in_other_room():
    s = bs().two_rooms().with_player()

    s.put_inventory(coin_silver)
    s.put_room(s.room_two, coin_copper)

    result = s.handle("look coin")

    assert_ok_message(result, tt.SILVER_COIN_DESCRIPTION)
    
    
def test_look_room_contents_do_not_require_container_behavior():
    world = World()

    room = world.add_room(names=(tt.ROOM_1,))
    world.current = room.id

    coin_entity = item(world, tt.COIN)
    world.put(room, coin_entity)

    result = world.handle("look")

    assert_ok_contains(result, tt.ROOM_1, tt.COIN)
    assert not room.has_behavior(Container.kind)


def test_look_target_inventory_does_not_require_container_behavior():
    world = World()

    room = world.add_room(names=(tt.ROOM_1,))
    world.current = room.id

    player = world.add(names=(tt.PLAYER,))
    world.player_id = player.id

    coin_entity = coin_copper(world)
    world.put(player, coin_entity)

    result = world.handle("look coin")

    assert_ok_message(result, tt.COPPER_COIN_DESCRIPTION)
    assert not player.has_behavior(Container.kind)