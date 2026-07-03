from twip.entity import Entity
from twip.extension import Openable, OpenState
from twip.world import World


def entity_with_openable(*, state: OpenState = OpenState.CLOSED) -> Entity:
    entity = Entity(
        names=("thing", "entity"),
        traits={"openable"},
    )
    entity.add_component(Openable(state=state))
    return entity


def test_open_closed_entity():
    world = World()
    entity = world.add(entity_with_openable(state=OpenState.CLOSED))

    result = world.handle("open thing")

    assert result.ok
    assert entity.component("openable").state == OpenState.OPEN


def test_open_already_open_entity():
    world = World()
    entity = world.add(entity_with_openable(state=OpenState.OPEN))

    result = world.handle("open thing")

    assert result.ok
    assert "already open" in result.message
    assert entity.component("openable").state == OpenState.OPEN


def test_close_open_entity():
    world = World()
    entity = world.add(entity_with_openable(state=OpenState.OPEN))

    result = world.handle("close thing")

    assert result.ok
    assert entity.component("openable").state == OpenState.CLOSED


def test_close_already_closed_entity():
    world = World()
    entity = world.add(entity_with_openable(state=OpenState.CLOSED))

    result = world.handle("close thing")

    assert result.ok
    assert "already closed" in result.message
    assert entity.component("openable").state == OpenState.CLOSED