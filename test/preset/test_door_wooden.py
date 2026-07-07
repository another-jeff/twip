from twip.behavior import Openable, OpenState
from twip.preset import door_wooden


def test_door_wooden_has_openable():
    entity = door_wooden()

    assert entity.behavior(Openable.kind).state == OpenState.CLOSED


def test_door_wooden_matches_door_name():
    entity = door_wooden()

    assert entity.matches("door")


def test_door_wooden_matches_wooden_door():
    entity = door_wooden()

    assert entity.matches("wooden door")


def test_door_wooden_does_not_match_wooden_without_name():
    entity = door_wooden()

    assert not entity.matches("wooden")