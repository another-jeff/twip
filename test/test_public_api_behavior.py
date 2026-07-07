# test/test_behavior_public_api.py

from twip.behavior import (
    Behavior,
    Containable,
    Container,
    Lookable,
    Openable,
    VerbMessageBehavior,
)


def test_behavior_public_api_exports_extension_building_blocks():
    assert Behavior
    assert VerbMessageBehavior


def test_behavior_public_api_exports_core_behaviors():
    assert Containable
    assert Container
    assert Lookable
    assert Openable


def test_behavior_public_api_does_not_export_pushable():
    import twip.behavior as behavior

    assert not hasattr(behavior, "Pushable")