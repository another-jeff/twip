from twip.behavior import Lockable, LockState, Openable, OpenState
from twip.preset import door_wooden_locked


def test_door_wooden_locked_has_openable():
    entity = door_wooden_locked()

    assert entity.behavior(Openable.kind).state == OpenState.CLOSED


def test_door_wooden_locked_has_lockable():
    entity = door_wooden_locked()

    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_door_wooden_locked_matches_door_name():
    entity = door_wooden_locked()

    assert entity.matches("door")


def test_door_wooden_locked_matches_wooden_door():
    entity = door_wooden_locked()

    assert entity.matches("wooden door")


def test_door_wooden_locked_does_not_match_wooden_without_name():
    entity = door_wooden_locked()

    assert not entity.matches("wooden")