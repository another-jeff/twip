from enum import Enum

from twip.component import Component
from twip.result import Result


class LockState(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"


class Lockable(Component):
    key = "lockable"

    def __init__(self, *, state: LockState = LockState.UNLOCKED):
        self.state = state

class Lockable(Component):
    key = "lockable"

    def __init__(self, *, state: LockState = LockState.UNLOCKED):
        self.state = state

    def handle(self, action, _entity, _world):
        if action.verb == "lock":
            return self.lock()

        if action.verb == "unlock":
            return self.unlock()

        return None

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