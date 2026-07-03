from twip.extension import OpenState
from twip.preset import door_wooden


def test_door_wooden_has_openable():
    entity = door_wooden()

    assert entity.component("openable").state == OpenState.CLOSED


def test_door_wooden_matches_door_alias():
    entity = door_wooden()

    assert entity.matches("door")