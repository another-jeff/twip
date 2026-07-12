from twip.behavior import (
    Containable,
    Container,
    Openable,
    OpenState,
)
from twip.world import World

from assertions import (
    assert_contains,
    assert_does_not_contain,
    assert_not_ok_contains,
    assert_ok_message,
)
from helpers import coin
from scenario import bs


def box(
    world: World,
    *,
    state: OpenState = OpenState.OPEN,
):
    return world.add(
        names=("box",),
        behaviors=(
            Containable(),
            Container(),
            Openable(state=state),
        ),
    )


def open_box(world: World):
    return box(world)


def closed_box(world: World):
    return box(world, state=OpenState.CLOSED)


def desk(world: World):
    return world.add(
        names=("desk",),
        behaviors=(Containable(),),
    )


def test_put_carried_item_in_open_container():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)
    box_entity = s.put_room(s.room_one, open_box)

    result = s.handle("put coin in box")

    assert_ok_message(
        result,
        "You put the coin in the box.",
    )
    assert_does_not_contain(s.player, coin_entity)
    assert_contains(box_entity, coin_entity)


def test_put_into_is_equivalent_to_put_in():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)
    box_entity = s.put_room(s.room_one, open_box)

    result = s.handle("put coin into box")

    assert_ok_message(
        result,
        "You put the coin in the box.",
    )
    assert_does_not_contain(s.player, coin_entity)
    assert_contains(box_entity, coin_entity)


def test_put_requires_carried_item():
    s = bs().one_room().with_player()
    coin_entity = s.put_room(s.room_one, coin)
    box_entity = s.put_room(s.room_one, open_box)

    result = s.handle("put coin in box")

    assert_not_ok_contains(result, "aren't carrying", "coin")
    assert_contains(s.room_one, coin_entity)
    assert_does_not_contain(box_entity, coin_entity)


def test_put_in_closed_container_fails_without_mutation():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)
    box_entity = s.put_room(s.room_one, closed_box)

    result = s.handle("put coin in box")

    assert_not_ok_contains(result, "box", "closed")
    assert_contains(s.player, coin_entity)
    assert_does_not_contain(box_entity, coin_entity)


def test_put_in_non_container_fails_without_mutation():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)
    s.put_room(s.room_one, desk)

    result = s.handle("put coin in desk")

    assert_not_ok_contains(result, "can't put", "desk")
    assert_contains(s.player, coin_entity)
    assert_does_not_contain(s.room_one, coin_entity)


def test_put_with_unsupported_relation_fails_without_mutation():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)
    box_entity = s.put_room(s.room_one, open_box)

    result = s.handle("put coin on box")

    assert_not_ok_contains(result, "can't put", "coin")
    assert_contains(s.player, coin_entity)
    assert_does_not_contain(box_entity, coin_entity)


def test_put_ignores_same_named_room_item():
    s = bs().one_room().with_player()
    room_coin = s.put_room(s.room_one, coin)
    carried_coin = s.put_inventory(coin)
    box_entity = s.put_room(s.room_one, open_box)

    result = s.handle("put coin in box")

    assert_ok_message(
        result,
        "You put the coin in the box.",
    )
    assert_contains(s.room_one, room_coin)
    assert_contains(box_entity, carried_coin)
    assert_does_not_contain(s.player, carried_coin)


def test_put_without_destination_fails_without_mutation():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)

    result = s.handle("put coin")

    assert_not_ok_contains(result, "Where", "coin")
    assert_contains(s.player, coin_entity)


def test_put_ambiguous_carried_item_fails_without_mutation():
    s = bs().one_room().with_player()
    first_coin = s.put_inventory(coin)
    second_coin = s.put_inventory(coin)
    box_entity = s.put_room(s.room_one, open_box)

    result = s.handle("put coin in box")

    assert_not_ok_contains(result, "Which coin")
    assert_contains(s.player, first_coin)
    assert_contains(s.player, second_coin)
    assert_does_not_contain(box_entity, first_coin)
    assert_does_not_contain(box_entity, second_coin)


def test_put_ambiguous_destination_fails_without_mutation():
    s = bs().one_room().with_player()
    coin_entity = s.put_inventory(coin)
    first_box = s.put_room(s.room_one, open_box)
    second_box = s.put_room(s.room_one, open_box)

    result = s.handle("put coin in box")

    assert_not_ok_contains(result, "Which box")
    assert_contains(s.player, coin_entity)
    assert_does_not_contain(first_box, coin_entity)
    assert_does_not_contain(second_box, coin_entity)