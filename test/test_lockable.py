from twip import World
from twip.extension import LockState
from twip.preset import door_wooden_locked


def test_lock_unlocked_door():
    world = World()
    world.add(door_wooden_locked(lock_state=LockState.UNLOCKED))

    result = world.handle("lock door")

    assert result.ok
    assert world.find("door_wooden_locked").component("lockable").state == LockState.LOCKED


def test_unlock_locked_door():
    world = World()
    world.add(door_wooden_locked(lock_state=LockState.LOCKED))

    result = world.handle("unlock door")

    assert result.ok
    assert world.find("door_wooden_locked").component("lockable").state == LockState.UNLOCKED


def test_lock_already_locked_door_fails_cleanly():
    world = World()
    world.add(door_wooden_locked(lock_state=LockState.LOCKED))

    result = world.handle("lock door")

    assert not result.ok
    assert "already locked" in result.message