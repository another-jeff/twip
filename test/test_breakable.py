# test/test_breakable.py

from twip.behavior import Containable
from twip.extensions import load_extension
from twip.world import World
from twip_ext.breakable import Breakable

from assertions import assert_not_ok_contains, assert_ok_message
from helpers import item
from scenario import bs


WINDOW = "window"
ROCK = "rock"

BREAK_MESSAGE = "The window shatters."
ALREADY_BROKEN_MESSAGE = "The window is already broken."


def breakable_window(world: World):
    return world.add(
        names=(WINDOW,),
        traits=set(),
        behaviors=(
            Containable(),
            Breakable(
                break_message=BREAK_MESSAGE,
                already_broken_message=ALREADY_BROKEN_MESSAGE,
            ),
        ),
    )


def plain_rock(world: World):
    return item(world, ROCK)


def test_break_breakable_target_succeeds(restore_verbs):
    load_extension("twip_ext.breakable")

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    result = s.handle("break window")

    assert_ok_message(result, BREAK_MESSAGE)


def test_break_already_broken_target_fails(restore_verbs):
    load_extension("twip_ext.breakable")

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    first = s.handle("break window")
    second = s.handle("break window")

    assert_ok_message(first, BREAK_MESSAGE)
    assert not second.ok
    assert second.message == ALREADY_BROKEN_MESSAGE


def test_break_non_breakable_target_fails_cleanly(restore_verbs):
    load_extension("twip_ext.breakable")

    s = bs().one_room()
    s.put_room(s.room_one, plain_rock)

    result = s.handle("break rock")

    assert_not_ok_contains(result, "can't do that")


def test_break_missing_target_asks_what(restore_verbs):
    load_extension("twip_ext.breakable")

    s = bs().one_room()

    result = s.handle("break")

    assert_not_ok_contains(result, "Break what")