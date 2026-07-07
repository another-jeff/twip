# test/test_readable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Containable, Readable


def readable_note(world):
    return world.add(
        names=("note",),
        traits=set(),
        behaviors=(
            Containable(),
            Readable("The note says: beware the cellar."),
        ),
    )


def test_read_readable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, readable_note)

    result = s.handle("read note")

    assert_ok_message(result, "The note says: beware the cellar.")


def test_read_readable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(readable_note)

    result = s.handle("read note")

    assert_ok_message(result, "The note says: beware the cellar.")