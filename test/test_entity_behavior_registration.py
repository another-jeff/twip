import pytest

from twip.behavior import Containable
from twip.entity import Entity


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