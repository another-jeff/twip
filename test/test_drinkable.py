# test/test_drinkable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Drinkable


def drinkable_water(world):
    return world.add(
        names=("water",),
        traits=set(),
        behaviors=(
            Drinkable("You drink the water. It tastes clean and cold."),
        ),
    )


def test_drink_drinkable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, drinkable_water)

    result = s.handle("drink water")

    assert_ok_message(result, "You drink the water. It tastes clean and cold.")


def test_drink_drinkable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(drinkable_water)

    result = s.handle("drink water")

    assert_ok_message(result, "You drink the water. It tastes clean and cold.")