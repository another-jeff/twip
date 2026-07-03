from twip.entity import Entity
from twip.extension import Openable, OpenState


def door_wooden(*, state: OpenState = OpenState.CLOSED) -> Entity:
    entity = Entity(
        key="door_wooden",
        name="wooden door",
        aliases={"door"},
    )

    entity.add_component(Openable(state=state))

    return entity