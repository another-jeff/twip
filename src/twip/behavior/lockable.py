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
        key_required_to_lock: bool = True,
        key_required_to_unlock: bool = True,
    ):
        self.state = state
        self.key_id = key_id
        self.key_required_to_lock = key_required_to_lock
        self.key_required_to_unlock = key_required_to_unlock

    def handle(self, action, _entity, world):
        if action.verb == "lock":
            if (
                self.key_id is not None
                and self.key_required_to_lock
                and not self.has_matching_key(action, world)
            ):
                return Result.failure("That key doesn't fit.")

            return self.lock()

        if action.verb == "unlock":
            if (
                self.key_id is not None
                and self.key_required_to_unlock
                and not self.has_matching_key(action, world)
            ):
                return Result.failure("That key doesn't fit.")

            return self.unlock()

        return None

    def has_matching_key(self, action, world) -> bool:
        if action.preposition != "with":
            return False

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