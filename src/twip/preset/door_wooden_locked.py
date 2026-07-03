from twip.entity import Entity
from twip.extension import Lockable, LockState, Openable, OpenState


def door_wooden_locked(
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
) -> Entity:
    entity = Entity(
        key="door_wooden_locked",
        name="locked wooden door",
        aliases={"door"},
    )

    entity.add_component(Openable(state=open_state))
    entity.add_component(Lockable(state=lock_state))

    return entity