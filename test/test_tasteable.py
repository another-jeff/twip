# test/test_tasteable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Containable, Tasteable


def tasteable_powder(world):
    return world.add(
        names=("powder",),
        traits=set(),
        behaviors=(
            Containable(),
            Tasteable("It tastes bitter and metallic."),
        ),
    )


def test_taste_tasteable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, tasteable_powder)

    result = s.handle("taste powder")

    assert_ok_message(result, "It tastes bitter and metallic.")


def test_taste_tasteable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(tasteable_powder)

    result = s.handle("taste powder")

    assert_ok_message(result, "It tastes bitter and metallic.")