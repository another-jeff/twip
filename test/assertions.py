from twip.entity import Entity
from twip.extension import Containable, Container


def assert_contains(container: Entity, entity: Entity):
    assert entity.id in container.component(Container.kind).items
    assert entity.component(Containable.kind).parent == container.id


def assert_does_not_contain(container: Entity, entity: Entity):
    assert entity.id not in container.component(Container.kind).items


def assert_ok_message(result, message: str):
    assert result.ok
    assert result.message == message


def assert_ok_contains(result, *parts: str):
    assert result.ok
    for part in parts:
        assert part in result.message


def assert_ok_omits(result, *parts: str):
    assert result.ok
    for part in parts:
        assert part not in result.message


def assert_not_ok_contains(result, *parts: str):
    assert not result.ok
    for part in parts:
        assert part in result.message


def assert_not_ok_contains_any(result, *parts: str):
    assert not result.ok
    message = result.message.lower()

    assert any(part.lower() in message for part in parts)