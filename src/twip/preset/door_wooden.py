from collections.abc import Iterable

from twip.entity import Entity
from twip.behavior import Openable, OpenState


def door_wooden(
    *,
    state: OpenState = OpenState.CLOSED,
    traits: Iterable[str] = (),
) -> Entity:
    entity = Entity(
        names=("door",),
        traits={"wooden", *traits},
    )

    entity.add_behavior(Openable(state=state))

    return entity