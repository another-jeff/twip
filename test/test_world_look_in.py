from twip.behavior import (
    Container,
    Openable,
    OpenState,
)
from twip.world import World

from assertions import (
    assert_not_ok_contains,
    assert_ok_contains,
    assert_ok_message,
    assert_ok_omits,
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
    

def test_look_into_is_equivalent_to_look_in():
    s = bs().one_room()

    box = s.put_room(
        s.room_one,
        box_factory(OpenState.OPEN),
    )
    coin = item(s.world, tt.COIN)
    s.world.put(box, coin)

    result = s.handle("look into box")

    assert_ok_message(
        result,
        "Inside the box, you see a coin.",
    )


def test_look_inside_is_equivalent_to_look_in():
    s = bs().one_room()

    box = s.put_room(
        s.room_one,
        box_factory(OpenState.OPEN),
    )
    coin = item(s.world, tt.COIN)
    s.world.put(box, coin)

    result = s.handle("look inside box")

    assert_ok_message(
        result,
        "Inside the box, you see a coin.",
    )
    
    
def test_look_in_lists_only_direct_contents():
    s = bs().one_room()

    outer_box = s.world.add(
        names=("box",),
        traits={"outer"},
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    inner_box = s.world.add(
        names=("box",),
        traits={"inner"},
        behaviors=(
            Container(),
            Openable(state=OpenState.OPEN),
        ),
    )
    coin = item(s.world, tt.COIN)

    s.world.put(s.room_one, outer_box)
    s.world.put(outer_box, inner_box)
    s.world.put(inner_box, coin)

    result = s.handle("look in outer box")

    assert_ok_contains(result, "a box")
    assert_ok_omits(result, tt.COIN)


def test_look_in_carried_open_container():
    s = bs().one_room().with_player()

    box = s.put_inventory(
        box_factory(OpenState.OPEN),
    )
    coin = item(s.world, tt.COIN)
    s.world.put(box, coin)

    result = s.handle("look in box")

    assert_ok_message(
        result,
        "Inside the box, you see a coin.",
    )