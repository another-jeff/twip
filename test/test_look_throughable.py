# test/test_look_throughable.py

from twip.behavior import Containable
from twip.extensions import load_extension
from twip.world import World
from twip_ext.breakable import Breakable
from twip_ext.look_throughable import LookThroughable
from twip_ext.shuttered import Shuttered

from assertions import assert_ok_message
from scenario import bs


WINDOW = "window"

BREAK_MESSAGE = "The window shatters."
VIEW_MESSAGE = "Through the window, you see a dark garden."
BROKEN_VIEW_MESSAGE = "Through the broken window, you see a dark garden."
SHUTTERED_MESSAGE = "The shutters are closed."


def breakable_window(world: World):
    return world.add(
        names=(WINDOW,),
        traits=set(),
        behaviors=(
            Containable(),
            Breakable(break_message=BREAK_MESSAGE),
            LookThroughable(
                view_message=VIEW_MESSAGE,
                broken_view_message=BROKEN_VIEW_MESSAGE,
            ),
        ),
    )


def shuttered_breakable_window(*, shutters_open: bool):
    def factory(world: World):
        return world.add(
            names=(WINDOW,),
            traits=set(),
            behaviors=(
                Containable(),
                Shuttered(
                    open=shutters_open,
                    closed_message=SHUTTERED_MESSAGE,
                ),
                Breakable(break_message=BREAK_MESSAGE),
                LookThroughable(
                    view_message=VIEW_MESSAGE,
                    broken_view_message=BROKEN_VIEW_MESSAGE,
                ),
            ),
        )

    return factory


def test_look_through_unbroken_window_succeeds(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_look_through_broken_window_uses_broken_view_message(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    s.handle("break window")
    result = s.handle("look through window")

    assert_ok_message(result, BROKEN_VIEW_MESSAGE)


def test_look_through_closed_shutters_fails(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.shuttered")

    s = bs().one_room()
    s.put_room(s.room_one, shuttered_breakable_window(shutters_open=False))

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == SHUTTERED_MESSAGE


def test_look_through_open_shutters_succeeds(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.shuttered")

    s = bs().one_room()
    s.put_room(s.room_one, shuttered_breakable_window(shutters_open=True))

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_look_through_closed_shutters_beat_broken_window(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.shuttered")

    s = bs().one_room()
    s.put_room(s.room_one, shuttered_breakable_window(shutters_open=False))

    s.handle("break window")
    result = s.handle("look through window")

    assert not result.ok
    assert result.message == SHUTTERED_MESSAGE