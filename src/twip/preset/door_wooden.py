from twip.entity import Entity
from twip.extension.door import Door, DoorState


def make_door_wooden(*, state: DoorState = DoorState.CLOSED) -> Entity:
    entity = Entity(
        key="door_wooden",
        name="wooden door",
    )

    entity.add_component(Door(state=state))

    return entity