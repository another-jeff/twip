import pytest

from twip.behavior import Containable, VerbMessageBehavior
from twip.entity import Entity


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

    entity.add_behavior(Containable())

    assert Containable.kind in entity.behaviors


def test_add_behavior_rejects_duplicate_kind_by_default():
    entity = Entity(names=("thing",))
    entity.add_behavior(Containable())

    with pytest.raises(ValueError, match="already attached"):
        entity.add_behavior(Containable())


def test_add_behavior_can_replace_behavior_when_explicit():
    entity = Entity(names=("thing",))
    first = Containable()
    second = Containable()

    entity.add_behavior(first)
    entity.add_behavior(second, replace=True)

    assert entity.behaviors[Containable.kind] is second


def test_add_behavior_rejects_different_behavior_with_same_kind():
    entity = Entity(names=("thing",))

    entity.add_behavior(FirstBehavior("first message"))

    with pytest.raises(ValueError, match="already attached"):
        entity.add_behavior(SecondBehavior("second message"))


def test_add_behavior_can_replace_different_behavior_with_same_kind_when_explicit():
    entity = Entity(names=("thing",))

    entity.add_behavior(FirstBehavior("first message"))
    entity.add_behavior(SecondBehavior("second message"), replace=True)

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