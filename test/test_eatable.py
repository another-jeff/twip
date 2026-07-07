# test/test_eatable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Containable, Eatable


def eatable_apple(world):
    return world.add(
        names=("apple",),
        traits=set(),
        behaviors=(
            Containable(),
            Eatable("You eat the apple. It is crisp and sharp."),
        ),
    )


def test_eat_eatable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, eatable_apple)

    result = s.handle("eat apple")

    assert_ok_message(result, "You eat the apple. It is crisp and sharp.")


def test_eat_eatable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(eatable_apple)

    result = s.handle("eat apple")

    assert_ok_message(result, "You eat the apple. It is crisp and sharp.")