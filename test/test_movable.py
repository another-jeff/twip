# test/test_movable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Movable


def movable_rock(world):
    return world.add(
        names=("rock",),
        traits=set(),
        behaviors=(
            Movable("The rock scrapes across the floor."),
        ),
    )


def test_move_movable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, movable_rock)

    result = s.handle("move rock")

    assert_ok_message(result, "The rock scrapes across the floor.")


def test_move_movable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(movable_rock)

    result = s.handle("move rock")

    assert_ok_message(result, "The rock scrapes across the floor.")