# test/test_look_throughable.py

from twip.behavior import Containable
from twip.extensions import load_extension
from twip.world import World
from twip_ext.breakable import Breakable
from twip_ext.look_throughable import LookThroughable
from twip_ext.shuttered import Shuttered
from twip_ext.blindered import Blindered

from assertions import assert_ok_message
from scenario import bs


WINDOW = "window"

BREAK_MESSAGE = "The window shatters."
VIEW_MESSAGE = "Through the window, you see a dark garden."
BROKEN_VIEW_MESSAGE = "Through the broken window, you see a dark garden."
SHUTTERED_MESSAGE = "The shutters are closed."
BLINDS_CLOSED_MESSAGE = "The blinds are closed."
BLINDS_OPEN_VIEW_MESSAGE = "Through the open blinds, you see a dark garden."
BLINDS = "blinds"
OPEN_BLINDS_MESSAGE = "You open the blinds."
CLOSE_BLINDS_MESSAGE = "You close the blinds."

def add_window_with_covering_blinds(
    s,
    *,
    blinds_raised: bool,
    blinds_open: bool,
):
    created = {}

    def window_factory(world: World):
        window = breakable_window(world)
        created["window"] = window
        return window

    def blinds_factory(world: World):
        window = created["window"]

        blinds = world.add(
            names=(BLINDS,),
            traits=set(),
            behaviors=(
                Containable(),
                Blindered(
                    raised=blinds_raised,
                    open=blinds_open,
                    covers=window.id,
                    closed_message=BLINDS_CLOSED_MESSAGE,
                    open_view_message=BLINDS_OPEN_VIEW_MESSAGE,
                    open_message=OPEN_BLINDS_MESSAGE,
                    close_message=CLOSE_BLINDS_MESSAGE,
                ),
            ),
        )

        created["blinds"] = blinds
        return blinds

    s.put_room(s.room_one, window_factory, blinds_factory)

    return created["window"], created["blinds"]



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


def blindered_breakable_window(*, blinds_raised: bool, blinds_open: bool):
    def factory(world: World):
        return world.add(
            names=(WINDOW,),
            traits=set(),
            behaviors=(
                Containable(),
                Blindered(
                    raised=blinds_raised,
                    open=blinds_open,
                    closed_message=BLINDS_CLOSED_MESSAGE,
                    open_view_message=BLINDS_OPEN_VIEW_MESSAGE,
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
    
    
def test_look_through_lowered_closed_blinds_fails(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    s.put_room(
        s.room_one,
        blindered_breakable_window(
            blinds_raised=False,
            blinds_open=False,
        ),
    )

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == BLINDS_CLOSED_MESSAGE


def test_look_through_lowered_open_blinds_succeeds_with_blinds_message(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    s.put_room(
        s.room_one,
        blindered_breakable_window(
            blinds_raised=False,
            blinds_open=True,
        ),
    )

    result = s.handle("look through window")

    assert_ok_message(result, BLINDS_OPEN_VIEW_MESSAGE)


def test_look_through_raised_blinds_uses_normal_view(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    s.put_room(
        s.room_one,
        blindered_breakable_window(
            blinds_raised=True,
            blinds_open=False,
        ),
    )

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_look_through_closed_blinds_beat_broken_window(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    s.put_room(
        s.room_one,
        blindered_breakable_window(
            blinds_raised=False,
            blinds_open=False,
        ),
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert not result.ok
    assert result.message == BLINDS_CLOSED_MESSAGE


def test_look_through_broken_window_beats_open_blinds_flavor(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    s.put_room(
        s.room_one,
        blindered_breakable_window(
            blinds_raised=False,
            blinds_open=True,
        ),
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert_ok_message(result, BROKEN_VIEW_MESSAGE)
    
    
def test_look_through_window_fails_when_external_blinds_cover_it_closed(
    restore_verbs,
):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    add_window_with_covering_blinds(
        s,
        blinds_raised=False,
        blinds_open=False,
    )

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == BLINDS_CLOSED_MESSAGE


def test_look_through_window_uses_external_open_blinds_view(
    restore_verbs,
):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    add_window_with_covering_blinds(
        s,
        blinds_raised=False,
        blinds_open=True,
    )

    result = s.handle("look through window")

    assert_ok_message(result, BLINDS_OPEN_VIEW_MESSAGE)


def test_look_through_window_ignores_external_raised_blinds(
    restore_verbs,
):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    add_window_with_covering_blinds(
        s,
        blinds_raised=True,
        blinds_open=False,
    )

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_external_closed_blinds_beat_broken_window(
    restore_verbs,
):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    add_window_with_covering_blinds(
        s,
        blinds_raised=False,
        blinds_open=False,
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert not result.ok
    assert result.message == BLINDS_CLOSED_MESSAGE
    
    
def test_open_blinds_opens_external_blinds_and_allows_view(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    _, blinds = add_window_with_covering_blinds(
        s,
        blinds_raised=False,
        blinds_open=False,
    )

    open_result = s.handle("open blinds")
    look_result = s.handle("look through window")

    assert_ok_message(open_result, OPEN_BLINDS_MESSAGE)
    assert blinds.behaviors[Blindered.kind].open
    assert_ok_message(look_result, BLINDS_OPEN_VIEW_MESSAGE)


def test_close_blinds_closes_external_blinds_and_blocks_view(restore_verbs):
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")
    load_extension("twip_ext.blindered")

    s = bs().one_room()
    _, blinds = add_window_with_covering_blinds(
        s,
        blinds_raised=False,
        blinds_open=True,
    )

    close_result = s.handle("close blinds")
    look_result = s.handle("look through window")

    assert_ok_message(close_result, CLOSE_BLINDS_MESSAGE)
    assert not blinds.behaviors[Blindered.kind].open
    assert not look_result.ok
    assert look_result.message == BLINDS_CLOSED_MESSAGE