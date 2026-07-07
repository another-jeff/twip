# test/test_searchable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Containable, Searchable


def searchable_desk(world):
    return world.add(
        names=("desk",),
        traits=set(),
        behaviors=(
            Containable(),
            Searchable("You find a tiny brass key taped underneath."),
        ),
    )


def test_search_searchable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, searchable_desk)

    result = s.handle("search desk")

    assert_ok_message(result, "You find a tiny brass key taped underneath.")


def test_search_searchable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(searchable_desk)

    result = s.handle("search desk")

    assert_ok_message(result, "You find a tiny brass key taped underneath.")