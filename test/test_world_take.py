from assertions import assert_contains, assert_does_not_contain
from helpers import coin, coin_blue, coin_red, statue
from scenario import bs

from twip.behavior import Container, Openable, OpenState
from twip.world import World


def test_take_visible_non_takeable_fails_without_mutation():
    s = bs().one_room().with_player()

    statue_entity = s.put_room(s.room_one, statue)

    result = s.handle("take statue")

    assert not result.ok
    assert_contains(s.room_one, statue_entity)
    assert_does_not_contain(s.player, statue_entity)


def test_take_disambiguated_visible_item_moves_only_that_item():
    s = bs().one_room().with_player()

    red = s.put_room(s.room_one, coin_red)
    blue = s.put_room(s.room_one, coin_blue)

    result = s.handle("take red coin")

    assert result.ok

    assert_does_not_contain(s.room_one, red)
    assert_contains(s.player, red)

    assert_contains(s.room_one, blue)
    assert_does_not_contain(s.player, blue)


def test_take_visible_containable_moves_it_to_player_inventory():
    s = bs().one_room().with_player()

    room_item = s.put_room(s.room_one, coin)

    result = s.handle("take coin")

    assert result.ok
    assert_does_not_contain(s.room_one, room_item)
    assert_contains(s.player, room_item)


def test_take_inventory_item_fails_without_mutation():
    s = bs().one_room().with_player()

    inventory_item = s.put_inventory(coin)

    result = s.handle("take coin")

    assert not result.ok
    assert_contains(s.player, inventory_item)
    assert_does_not_contain(s.room_one, inventory_item)


def test_take_without_player_fails_without_mutation():
    s = bs().one_room()

    room_item = s.put_room(s.room_one, coin)

    result = s.handle("take coin")

    assert not result.ok
    assert_contains(s.room_one, room_item)


def test_take_same_named_item_in_other_room_does_not_create_ambiguity():
    s = bs().two_rooms().with_player()

    room_item = s.put_room(s.room_one, coin)
    other_room_item = s.put_room(s.room_two, coin)

    result = s.handle("take coin")

    assert result.ok

    assert_does_not_contain(s.room_one, room_item)
    assert_contains(s.player, room_item)

    assert_contains(s.room_two, other_room_item)
    assert_does_not_contain(s.player, other_room_item)


def test_take_ignores_same_named_inventory_item_after_prior_take():
    s = bs().one_room().with_player()

    red = s.put_room(s.room_one, coin_red)
    blue = s.put_room(s.room_one, coin_blue)

    first_result = s.handle("take red coin")
    second_result = s.handle("take coin")

    assert first_result.ok
    assert second_result.ok

    assert_contains(s.player, red)
    assert_contains(s.player, blue)
    
    
def test_take_non_takeable_uses_resolved_entity_name():
    s = bs().one_room().with_player()

    statue_entity = statue(s.world)
    statue_entity.traits.add("stone")
    s.world.put(s.room_one, statue_entity)

    result = s.handle("take stone statue")

    assert not result.ok
    assert result.message == "You can't take the statue."
    assert_contains(s.room_one, statue_entity)
    assert_does_not_contain(s.player, statue_entity)
    
    
def test_take_does_not_require_player_container_behavior():
    world = World()

    room = world.add_room(names=("room",))
    world.current = room.id

    player = world.add(names=("player",))
    world.player_id = player.id

    coin_entity = coin(world)
    world.put(room, coin_entity)

    result = world.handle("take coin")

    assert result.ok
    assert not player.has_behavior(Container.kind)
    assert world.contents_of(room) == []
    assert world.contents_of(player) == [coin_entity]
    assert coin_entity.parent == player.id


def test_take_from_nested_open_containers():
    s = bs().one_room().with_player()

    outer_box = s.world.add(
        names=("outer box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    inner_box = s.world.add(
        names=("inner box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    coin_entity = coin(s.world)

    s.world.put(s.room_one, outer_box)
    s.world.put(outer_box, inner_box)
    s.world.put(inner_box, coin_entity)

    result = s.handle("take coin")

    assert result.ok
    assert_contains(s.player, coin_entity)
    assert_does_not_contain(inner_box, coin_entity)


def test_take_through_closed_outer_container_fails_without_mutation():
    s = bs().one_room().with_player()

    outer_box = s.world.add(
        names=("outer box",),
        behaviors=(
            Container(),
            Openable(),
        ),
    )
    inner_box = s.world.add(
        names=("inner box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    coin_entity = coin(s.world)

    s.world.put(s.room_one, outer_box)
    s.world.put(outer_box, inner_box)
    s.world.put(inner_box, coin_entity)

    result = s.handle("take coin")

    assert not result.ok
    assert_contains(inner_box, coin_entity)
    assert_does_not_contain(s.player, coin_entity)


def test_take_through_closed_inner_container_fails_without_mutation():
    s = bs().one_room().with_player()

    outer_box = s.world.add(
        names=("outer box",),
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    inner_box = s.world.add(
        names=("inner box",),
        behaviors=(
            Container(),
            Openable(),
        ),
    )
    coin_entity = coin(s.world)

    s.world.put(s.room_one, outer_box)
    s.world.put(outer_box, inner_box)
    s.world.put(inner_box, coin_entity)

    result = s.handle("take coin")

    assert not result.ok
    assert_contains(inner_box, coin_entity)
    assert_does_not_contain(s.player, coin_entity)