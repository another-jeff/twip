from twip.entity import Entity
from twip.extension.door import Door


def make_door_wooden(*, is_open: bool = False) -> Entity:
    entity = Entity(
        key="door_wooden",
        name="wooden door",
    )

    entity.add_component(Door(is_open=is_open))

    return entity