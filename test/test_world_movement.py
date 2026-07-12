from twip.behavior import Lockable, LockState, Openable, OpenState

from helpers import item
from scenario import bs

import tt


def test_go_direction_moves_to_connected_room():
    s = bs().two_rooms()
    s.connect()

    result = s.handle("go north")

    assert result.ok
    assert result.message == "You go north."
    assert s.world.current == s.room_two.id


def test_go_unknown_direction_fails_cleanly():
    s = bs().two_rooms()

    result = s.handle("go north")

    assert not result.ok
    assert result.message == "You can't go that way."
    assert s.world.current == s.room_one.id


def test_go_direction_through_closed_door_fails_cleanly():
    s = bs().two_rooms()

    s.connect(behaviors=(Openable(state=OpenState.CLOSED),))

    result = s.handle("go north")

    assert not result.ok
    assert s.world.current == s.room_one.id


def test_go_direction_through_open_door_moves_to_connected_room():
    s = bs().two_rooms()

    s.connect(behaviors=(Openable(state=OpenState.OPEN),))

    result = s.handle("go north")

    assert result.ok
    assert s.world.current == s.room_two.id


def test_movement_changes_visible_room_contents():
    s = bs().two_rooms()

    coin = item(s.world, tt.COIN)
    gem = item(s.world, tt.GEM)

    s.world.contain(s.room_one, coin)
    s.world.contain(s.room_two, gem)

    s.connect()

    assert s.world.find(tt.COIN) is coin
    assert s.world.find(tt.GEM) is None

    result = s.handle("go north")

    assert result.ok
    assert s.world.current == s.room_two.id
    assert s.world.find(tt.COIN) is None
    assert s.world.find(tt.GEM) is gem


def test_go_ambiguous_direction_fails_without_moving():
    s = bs().three_rooms()

    s.connect(traits={tt.WOODEN})
    s.connect(s.room_three, traits={tt.STONE})

    result = s.handle("go north")

    assert not result.ok
    assert s.world.current == s.room_one.id


def test_go_direction_with_connector_traits_resolves_ambiguous_exit():
    s = bs().three_rooms()

    s.connect(traits={tt.WOODEN})
    s.connect(s.room_three, traits={tt.STONE})

    result = s.handle("go north wooden door")

    assert result.ok
    assert s.world.current == s.room_two.id


def test_go_direction_with_connector_traits_through_closed_door_fails():
    s = bs().two_rooms()

    s.connect(
        traits={tt.WOODEN},
        behaviors=(Openable(state=OpenState.CLOSED),),
    )

    result = s.handle("go north wooden door")

    assert not result.ok
    assert s.world.current == s.room_one.id


def test_open_door_then_go_direction_moves_to_connected_room():
    s = bs().two_rooms()

    s.connect(behaviors=(Openable(state=OpenState.CLOSED),))

    go_closed = s.handle("go north")

    assert not go_closed.ok
    assert s.world.current == s.room_one.id

    opened = s.handle("open north door")

    assert opened.ok

    go_open = s.handle("go north")

    assert go_open.ok
    assert s.world.current == s.room_two.id


def test_movement_uses_other_side_direction_after_room_changes():
    s = bs().two_rooms()

    s.connect()

    north = s.handle("go north")

    assert north.ok
    assert s.world.current == s.room_two.id

    wrong_way = s.handle("go north")

    assert not wrong_way.ok
    assert s.world.current == s.room_two.id

    south = s.handle("go south")

    assert south.ok
    assert s.world.current == s.room_one.id


def test_locked_closed_door_cannot_be_opened_or_moved_through():
    s = bs().two_rooms()

    s.connect(
        behaviors=(
            Openable(state=OpenState.CLOSED),
            Lockable(state=LockState.LOCKED),
        ),
    )

    opened = s.handle("open north door")

    assert not opened.ok
    assert s.world.current == s.room_one.id

    moved = s.handle("go north")

    assert not moved.ok
    assert s.world.current == s.room_one.id


def test_unlock_open_then_go_moves_through_door():
    s = bs().two_rooms()

    s.connect(
        behaviors=(
            Openable(state=OpenState.CLOSED),
            Lockable(state=LockState.LOCKED),
        ),
    )

    unlocked = s.handle("unlock north door")

    assert unlocked.ok

    opened = s.handle("open north door")

    assert opened.ok

    moved = s.handle("go north")

    assert moved.ok
    assert s.world.current == s.room_two.id


def test_go_connector_without_side_direction_fails_without_moving():
    s = bs().two_rooms()

    s.connect(traits={tt.WOODEN})

    result = s.handle("go wooden door")

    assert not result.ok
    assert s.world.current == s.room_one.id