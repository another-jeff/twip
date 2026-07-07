from collections.abc import Iterable

from twip.entity import Entity
from twip.behavior import Lockable, LockState, Openable, OpenState


def door_wooden_locked(
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
    traits: Iterable[str] = (),
) -> Entity:
    entity = Entity(
        names=("door",),
        traits={"wooden", *traits},
    )

    entity.add_behavior(Openable(state=open_state))
    entity.add_behavior(Lockable(state=lock_state))

    return entity