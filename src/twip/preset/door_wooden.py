from twip.entity import Entity
from twip.extension import Openable, OpenState


def make_door_wooden(*, state: OpenState = OpenState.CLOSED) -> Entity:
    entity = Entity(
        key="door_wooden",
        name="wooden door",
        aliases={"door"},
    )

    entity.add_component(Openable(state=state))

    return entity