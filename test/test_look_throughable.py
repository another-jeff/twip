# test/test_look_throughable.py

from twip.behavior import Containable
from twip.extensions import load_extension
from twip.world import World
from twip_ext.breakable import Breakable
from twip_ext.look_throughable import LookThroughable
from twip_ext.view_covering import ViewCovering

from assertions import assert_ok_message
from scenario import bs


WINDOW = "window"
BLINDS = "blinds"
CURTAINS = "curtains"

BREAK_MESSAGE = "The window shatters."
VIEW_MESSAGE = "Through the window, you see a dark garden."
BROKEN_VIEW_MESSAGE = "Through the broken window, you see a dark garden."

SHUTTERS_CLOSED_MESSAGE = "The shutters are closed."

COVERING_CLOSED_MESSAGE = "The blinds are closed."
COVERING_OPEN_VIEW_MESSAGE = "Through the open blinds, you see a dark garden."
OPEN_COVERING_MESSAGE = "You open the blinds."
CLOSE_COVERING_MESSAGE = "You close the blinds."

OPEN_CURTAINS_MESSAGE = "You open the curtains."


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


def view_covered_breakable_window(
    *,
    covering: bool,
    covering_open: bool,
    closed_message: str = COVERING_CLOSED_MESSAGE,
    open_view_message: str | None = COVERING_OPEN_VIEW_MESSAGE,
    open_message: str = OPEN_COVERING_MESSAGE,
    close_message: str = CLOSE_COVERING_MESSAGE,
    open_uncovers: bool = False,
):
    def factory(world: World):
        return world.add(
            names=(WINDOW,),
            traits=set(),
            behaviors=(
                Containable(),
                ViewCovering(
                    covering=covering,
                    open=covering_open,
                    closed_message=closed_message,
                    open_view_message=open_view_message,
                    open_message=open_message,
                    close_message=close_message,
                    open_uncovers=open_uncovers,
                ),
                Breakable(break_message=BREAK_MESSAGE),
                LookThroughable(
                    view_message=VIEW_MESSAGE,
                    broken_view_message=BROKEN_VIEW_MESSAGE,
                ),
            ),
        )

    return factory


def add_window_with_view_covering(
    s,
    *,
    covering_name: str,
    covering: bool,
    covering_open: bool,
    closed_message: str = COVERING_CLOSED_MESSAGE,
    open_view_message: str | None = COVERING_OPEN_VIEW_MESSAGE,
    open_message: str = OPEN_COVERING_MESSAGE,
    close_message: str = CLOSE_COVERING_MESSAGE,
    open_uncovers: bool = False,
):
    created = {}

    def window_factory(world: World):
        window = breakable_window(world)
        created["window"] = window
        return window

    def covering_factory(world: World):
        window = created["window"]

        view_cover = world.add(
            names=(covering_name,),
            traits=set(),
            behaviors=(
                Containable(),
                ViewCovering(
                    covers=window.id,
                    covering=covering,
                    open=covering_open,
                    closed_message=closed_message,
                    open_view_message=open_view_message,
                    open_message=open_message,
                    close_message=close_message,
                    open_uncovers=open_uncovers,
                ),
            ),
        )

        created["covering"] = view_cover
        return view_cover

    s.put_room(s.room_one, window_factory, covering_factory)

    return created["window"], created["covering"]


def load_look_through_extensions():
    load_extension("twip_ext.breakable")
    load_extension("twip_ext.look_throughable")


def load_view_covering_extensions():
    load_look_through_extensions()
    load_extension("twip_ext.view_covering")


def test_look_through_unbroken_window_succeeds(restore_verbs):
    load_look_through_extensions()

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_look_through_broken_window_uses_broken_view_message(restore_verbs):
    load_look_through_extensions()

    s = bs().one_room()
    s.put_room(s.room_one, breakable_window)

    s.handle("break window")
    result = s.handle("look through window")

    assert_ok_message(result, BROKEN_VIEW_MESSAGE)


def test_look_through_closed_shutters_fails(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=True,
            covering_open=False,
            closed_message=SHUTTERS_CLOSED_MESSAGE,
            open_view_message=None,
            open_uncovers=True,
        ),
    )

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == SHUTTERS_CLOSED_MESSAGE


def test_look_through_open_shutters_succeeds(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=False,
            covering_open=True,
            closed_message=SHUTTERS_CLOSED_MESSAGE,
            open_view_message=None,
            open_uncovers=True,
        ),
    )

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_look_through_closed_shutters_beat_broken_window(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=True,
            covering_open=False,
            closed_message=SHUTTERS_CLOSED_MESSAGE,
            open_view_message=None,
            open_uncovers=True,
        ),
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert not result.ok
    assert result.message == SHUTTERS_CLOSED_MESSAGE


def test_look_through_same_entity_view_covering_closed_fails(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=True,
            covering_open=False,
        ),
    )

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == COVERING_CLOSED_MESSAGE


def test_look_through_same_entity_view_covering_open_uses_covering_message(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=True,
            covering_open=True,
        ),
    )

    result = s.handle("look through window")

    assert_ok_message(result, COVERING_OPEN_VIEW_MESSAGE)


def test_look_through_same_entity_view_covering_uncovered_uses_normal_view(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=False,
            covering_open=False,
        ),
    )

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_look_through_same_entity_closed_view_covering_beats_broken_window(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=True,
            covering_open=False,
        ),
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert not result.ok
    assert result.message == COVERING_CLOSED_MESSAGE


def test_look_through_broken_window_beats_same_entity_open_covering_flavor(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    s.put_room(
        s.room_one,
        view_covered_breakable_window(
            covering=True,
            covering_open=True,
        ),
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert_ok_message(result, BROKEN_VIEW_MESSAGE)


def test_look_through_window_fails_when_external_view_covering_is_closed(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=True,
        covering_open=False,
    )

    result = s.handle("look through window")

    assert not result.ok
    assert result.message == COVERING_CLOSED_MESSAGE


def test_look_through_window_uses_external_open_view_covering_message(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=True,
        covering_open=True,
    )

    result = s.handle("look through window")

    assert_ok_message(result, COVERING_OPEN_VIEW_MESSAGE)


def test_look_through_window_ignores_external_view_covering_when_uncovered(
    restore_verbs,
):
    load_view_covering_extensions()

    s = bs().one_room()
    add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=False,
        covering_open=False,
    )

    result = s.handle("look through window")

    assert_ok_message(result, VIEW_MESSAGE)


def test_external_closed_view_covering_beats_broken_window(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=True,
        covering_open=False,
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert not result.ok
    assert result.message == COVERING_CLOSED_MESSAGE


def test_broken_window_beats_external_open_view_covering_flavor(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=True,
        covering_open=True,
    )

    s.handle("break window")
    result = s.handle("look through window")

    assert_ok_message(result, BROKEN_VIEW_MESSAGE)


def test_open_external_view_covering_allows_view(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    _, covering = add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=True,
        covering_open=False,
    )

    open_result = s.handle("open blinds")
    look_result = s.handle("look through window")

    assert_ok_message(open_result, OPEN_COVERING_MESSAGE)
    assert covering.behaviors[ViewCovering.kind].open
    assert_ok_message(look_result, COVERING_OPEN_VIEW_MESSAGE)


def test_close_external_view_covering_blocks_view(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    _, covering = add_window_with_view_covering(
        s,
        covering_name=BLINDS,
        covering=True,
        covering_open=True,
    )

    close_result = s.handle("close blinds")
    look_result = s.handle("look through window")

    assert_ok_message(close_result, CLOSE_COVERING_MESSAGE)
    assert not covering.behaviors[ViewCovering.kind].open
    assert not look_result.ok
    assert look_result.message == COVERING_CLOSED_MESSAGE


def test_open_external_view_covering_can_uncover_window(restore_verbs):
    load_view_covering_extensions()

    s = bs().one_room()
    _, curtains = add_window_with_view_covering(
        s,
        covering_name=CURTAINS,
        covering=True,
        covering_open=False,
        open_message=OPEN_CURTAINS_MESSAGE,
        open_uncovers=True,
    )

    open_result = s.handle("open curtains")
    look_result = s.handle("look through window")

    assert_ok_message(open_result, OPEN_CURTAINS_MESSAGE)
    assert not curtains.behaviors[ViewCovering.kind].covering
    assert_ok_message(look_result, VIEW_MESSAGE)