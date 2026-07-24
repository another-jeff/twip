import tt
from twip.behavior import Lockable, LockState, Openable, OpenState
from twip.world import World


def add_openable_lockable(
    world: World,
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
    key_id: str | None = None,
):
    return world.add(
        names=(tt.THING,),
        behaviors=(
            Openable(state=open_state),
            Lockable(state=lock_state, key_id=key_id),
        ),
    )


def test_open_locked_entity_fails():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.LOCKED)

    result = world.handle("open thing")

    assert not result.ok
    assert "locked" in result.message
    assert entity.behavior(Openable.kind).state == OpenState.CLOSED


def test_open_unlocked_entity_succeeds():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.UNLOCKED)

    result = world.handle("open thing")

    assert result.ok
    assert entity.behavior(Openable.kind).state == OpenState.OPEN


def test_unlock_keyed_entity_with_wrong_key_fails():
    world = World()
    key = world.add(names=("key",))
    world.add(names=("wrong key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    result = world.handle("unlock thing with wrong key")

    assert not result.ok
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED