import tt

from twip.extension import Lockable, LockState, Openable, OpenState
from twip.world import World


def add_openable_lockable(
    world: World,
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
):
    return world.add(
        names=(tt.THING,),
        components=(
            Openable(state=open_state),
            Lockable(state=lock_state),
        ),
    )


def test_open_locked_entity_fails():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.LOCKED)

    result = world.handle("open thing")

    assert not result.ok
    assert "locked" in result.message
    assert entity.component(Openable.id).state == OpenState.CLOSED


def test_open_unlocked_entity_succeeds():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.UNLOCKED)

    result = world.handle("open thing")

    assert result.ok
    assert entity.component(Openable.id).state == OpenState.OPEN