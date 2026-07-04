import tt

from twip.extension import Openable, OpenState
from twip.world import World


def add_openable(
    world: World,
    *,
    state: OpenState = OpenState.CLOSED,
):
    return world.add(
        names=(tt.THING,),
        components=(Openable(state=state),),
    )


def test_open_closed_entity():
    world = World()
    entity = add_openable(world, state=OpenState.CLOSED)

    result = world.handle("open thing")

    assert result.ok
    assert entity.component(Openable.id).state == OpenState.OPEN


def test_open_already_open_entity():
    world = World()
    entity = add_openable(world, state=OpenState.OPEN)

    result = world.handle("open thing")

    assert result.ok
    assert "already open" in result.message
    assert entity.component(Openable.id).state == OpenState.OPEN


def test_close_open_entity():
    world = World()
    entity = add_openable(world, state=OpenState.OPEN)

    result = world.handle("close thing")

    assert result.ok
    assert entity.component(Openable.id).state == OpenState.CLOSED


def test_close_already_closed_entity():
    world = World()
    entity = add_openable(world, state=OpenState.CLOSED)

    result = world.handle("close thing")

    assert result.ok
    assert "already closed" in result.message
    assert entity.component(Openable.id).state == OpenState.CLOSED