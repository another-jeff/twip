# test/test_touchable.py

from assertions import assert_ok_message
from scenario import bs
from twip.extension import Containable, Touchable


def touchable_stone(world):
    return world.add(
        names=("stone",),
        traits=set(),
        components=(
            Containable(),
            Touchable("The stone is cold and faintly damp."),
        ),
    )


def test_touch_touchable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, touchable_stone)

    result = s.handle("touch stone")

    assert_ok_message(result, "The stone is cold and faintly damp.")


def test_touch_touchable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(touchable_stone)

    result = s.handle("touch stone")

    assert_ok_message(result, "The stone is cold and faintly damp.")