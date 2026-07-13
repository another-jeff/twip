from twip.behavior import (
    Container,
    Openable,
    OpenState,
)
from twip.world import World

from assertions import (
    assert_not_ok_contains,
    assert_ok_message,
)
from helpers import item
from scenario import bs

import tt


def box_factory(
    state: OpenState = OpenState.CLOSED,
):
    def make(world: World):
        return world.add(
            names=("box",),
            behaviors=(
                Container(),
                Openable(state=state),
            ),
        )

    return make


def test_look_in_closed_container_reports_closed():
    s = bs().one_room()
    box = s.put_room(s.room_one, box_factory())
    coin = item(s.world, tt.COIN)
    s.world.put(box, coin)

    result = s.handle("look in box")

    assert_not_ok_contains(result, "box", "closed")
    assert tt.COIN not in result.message


def test_look_in_open_empty_container_reports_empty():
    s = bs().one_room()
    s.put_room(
        s.room_one,
        box_factory(OpenState.OPEN),
    )

    result = s.handle("look in box")

    assert_ok_message(result, "The box is empty.")


def test_look_in_open_populated_container_lists_contents():
    s = bs().one_room()
    box = s.put_room(
        s.room_one,
        box_factory(OpenState.OPEN),
    )
    coin = item(s.world, tt.COIN)
    s.world.put(box, coin)

    result = s.handle("look in box")

    assert_ok_message(
        result,
        "Inside the box, you see a coin.",
    )