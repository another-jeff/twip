# test/test_look_throughable.py

from twip.behavior import Containable
from twip.extensions import load_extension
from twip.world import World
from twip_ext.breakable import Breakable
from twip_ext.look_throughable import LookThroughable

from assertions import assert_ok_message
from scenario import bs


WINDOW = "window"

BLOCKED_MESSAGE = "The window is too grimy to see through."
BREAK_MESSAGE = "The window shatters."
VIEW_MESSAGE = "Through the broken window, you see a dark garden."


def breakable_window(world: World):
    return world.add(
        names=(WINDOW,),
        traits=set(),
        behaviors=(
            Containable(),
            Breakable(break_message=BREAK_MESSAGE),
            LookThroughable(
                blocked_message=BLOCKED_MESSAGE,
                view_message=VIEW_MESSAGE,
            ),
        ),
    )


def test_look_through_unbroken_window_fails_with_blocked_message(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == BLOCKED_MESSAGE


def test_look_through_broken_window_succeeds(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    s.handle("break window")
    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)