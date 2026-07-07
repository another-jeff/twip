# test/test_turnable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Containable, Turnable


def turnable_knob(world):
    return world.add(
        names=("knob",),
        traits=set(),
        behaviors=(
            Containable(),
            Turnable("The knob turns with a soft click."),
        ),
    )


def test_turn_turnable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, turnable_knob)

    result = s.handle("turn knob")

    assert_ok_message(result, "The knob turns with a soft click.")


def test_turn_turnable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(turnable_knob)

    result = s.handle("turn knob")

    assert_ok_message(result, "The knob turns with a soft click.")