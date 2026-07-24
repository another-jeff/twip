from __future__ import annotations

from enum import Enum
from typing import ClassVar

from twip.behavior.base import Behavior
from twip.result import Result


class LockState(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"


class Lockable(Behavior):
    kind: ClassVar[str] = "lockable"

    def __init__(
        self,
        *,
        state: LockState = LockState.UNLOCKED,
        key_id: str | None = None,
    ):
        self.state = state
        self.key_id = key_id

    def handle(self, action, _entity, world):
        if action.verb == "lock":
            if self.key_id is not None and not self.has_matching_key(action, world):
                return Result.failure("That key doesn't fit.")

            return self.lock()

        if action.verb == "unlock":
            if self.key_id is not None and not self.has_matching_key(action, world):
                return Result.failure("That key doesn't fit.")

            return self.unlock()

        return None

    def has_matching_key(self, action, world) -> bool:
        keys = world.find_reachable_all(action.target_indirect or "")

        return any(
            key.id == self.key_id
            and key.parent == world.player_id
            for key in keys
        )

    def lock(self) -> Result:
        if self.state == LockState.LOCKED:
            return Result.failure("It's already locked.")

        self.state = LockState.LOCKED

        return Result.success("Locked.")

    def unlock(self) -> Result:
        if self.state == LockState.UNLOCKED:
            return Result.failure("It's already unlocked.")

        self.state = LockState.UNLOCKED

        return Result.success("Unlocked.")
    
def test_lock_keyed_entity_with_correct_carried_key_succeeds():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, key)
    world.put(room, entity)

    result = world.handle("lock thing with key")

    assert result.ok
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_lock_keyed_entity_with_wrong_carried_key_fails():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    wrong_key = world.add(names=("wrong key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, wrong_key)
    world.put(room, entity)

    result = world.handle("lock thing with wrong key")

    assert not result.ok
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED