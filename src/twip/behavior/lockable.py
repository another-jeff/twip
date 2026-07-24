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
            return self.change_state(
                action,
                world,
                target_state=LockState.LOCKED,
                key_required=self.key_required_to_lock,
            )

        if action.verb == "unlock":
            return self.change_state(
                action,
                world,
                target_state=LockState.UNLOCKED,
                key_required=self.key_required_to_unlock,
            )

        return None
    
    def change_state(
        self,
        action,
        world,
        *,
        target_state: LockState,
        key_required: bool,
    ) -> Result:
        failure = self.validate_key(
            action,
            world,
            required=key_required,
        )
        if failure is not None:
            return failure

        failure = self.validate_state(world, target_state)
        if failure is not None:
            return failure

        self.set_state(target_state)

        return self.report_state_change(world, target_state)

    def validate_key(self, action, world, *, required: bool) -> Result | None:
        if self.key_id is None or not required:
            return None

        if not self.has_matching_key(action, world):
            return Result.failure(world.language.key_does_not_fit())

        return None

    def find_supplied_keys(self, action, world):
        if action.preposition != "with":
            return []

        if action.target_indirect is None:
            return []

        keys = world.find_reachable_all(action.target_indirect)

        return [
            key
            for key in keys
            if key.parent == world.player_id
        ]

    def has_matching_key(self, action, world) -> bool:
        keys = self.find_supplied_keys(action, world)

        return any(key.id == self.key_id for key in keys)

    def set_state(self, state: LockState) -> None:
        self.state = state
        
    def report_state_change(
        self,
        world,
        state: LockState,
    ) -> Result:
        if state == LockState.LOCKED:
            return Result.success(world.language.lock_success())

        return Result.success(world.language.unlock_success())
    
    def validate_state(
        self,
        world,
        target_state: LockState,
    ) -> Result | None:
        if self.state != target_state:
            return None

        if target_state == LockState.LOCKED:
            return Result.failure(world.language.already_locked())

        return Result.failure(world.language.already_unlocked())