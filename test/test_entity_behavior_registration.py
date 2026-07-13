import pytest

from twip.behavior import VerbMessageBehavior
from twip.entity import Entity


class MundaneBehavior(VerbMessageBehavior):
    kind = "test"
    verb = "test"


class FirstBehavior(VerbMessageBehavior):
    kind = "same"
    verb = "first"


class SecondBehavior(VerbMessageBehavior):
    kind = "same"
    verb = "second"


class OtherBehavior(VerbMessageBehavior):
    kind = "other"
    verb = "other"


def test_add_behavior_adds_behavior_by_kind():
    entity = Entity(names=("thing",))

    entity.add_behavior(MundaneBehavior("test message"))

    assert MundaneBehavior.kind in entity.behaviors


def test_add_behavior_rejects_duplicate_kind_by_default():
    entity = Entity(names=("thing",))
    entity.add_behavior(MundaneBehavior("first message"))

    with pytest.raises(ValueError, match="already attached"):
        entity.add_behavior(MundaneBehavior("second message"))


def test_add_behavior_can_replace_behavior_when_explicit():
    entity = Entity(names=("thing",))
    first = MundaneBehavior("first message")
    second = MundaneBehavior("second message")

    entity.add_behavior(first)
    entity.add_behavior(second, replace=True)

    assert entity.behaviors[MundaneBehavior.kind] is second


def test_add_behavior_rejects_different_behavior_with_same_kind():
    entity = Entity(names=("thing",))

    entity.add_behavior(FirstBehavior("first message"))

    with pytest.raises(ValueError, match="already attached"):
        entity.add_behavior(SecondBehavior("second message"))


def test_add_behavior_can_replace_different_behavior_with_same_kind_when_explicit():
    entity = Entity(names=("thing",))

    entity.add_behavior(FirstBehavior("first message"))
    entity.add_behavior(
        SecondBehavior("second message"),
        replace=True,
    )

    assert isinstance(entity.behaviors["same"], SecondBehavior)
    assert entity.behaviors["same"].message == "second message"


def test_add_behavior_accepts_multiple_different_behavior_kinds():
    entity = Entity(names=("thing",))

    entity.add_behavior(
        FirstBehavior("first message"),
        OtherBehavior("other message"),
    )

    assert isinstance(entity.behaviors["same"], FirstBehavior)
    assert isinstance(entity.behaviors["other"], OtherBehavior)