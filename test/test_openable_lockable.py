from twip.entity import Entity
from twip.extension import Lockable, LockState, Openable, OpenState
from twip.world import World


def entity_with_openable_lockable(
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
) -> Entity:
    entity = Entity(
        names=("thing", "entity"),
        traits={"openable", "lockable"},
    )
    entity.add_component(Openable(state=open_state))
    entity.add_component(Lockable(state=lock_state))
    return entity


def test_open_locked_entity_fails():
    world = World()
    entity = world.add(
        entity_with_openable_lockable(lock_state=LockState.LOCKED)
    )

    result = world.handle("open thing")

    assert not result.ok
    assert "locked" in result.message
    assert entity.component("openable").state == OpenState.CLOSED


def test_open_unlocked_entity_succeeds():
    world = World()
    entity = world.add(
        entity_with_openable_lockable(lock_state=LockState.UNLOCKED)
    )

    result = world.handle("open thing")

    assert result.ok
    assert entity.component("openable").state == OpenState.OPEN