from twip.extension import LockState, OpenState
from twip.preset import door_wooden_locked


def test_door_wooden_locked_has_openable():
    entity = door_wooden_locked()

    assert entity.component("openable").state == OpenState.CLOSED


def test_door_wooden_locked_has_lockable():
    entity = door_wooden_locked()

    assert entity.component("lockable").state == LockState.LOCKED


def test_door_wooden_locked_matches_door_alias():
    entity = door_wooden_locked()

    assert entity.matches("door")