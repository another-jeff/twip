from twip.extension import Containable, Container, Lookable
from twip.world import World


def world_with_lookable_item() -> World:
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    lamp = world.add(
        names=("lamp",),
        traits=set(),
        components=(
            Containable(),
            Lookable("A brass lamp with a green shade."),
        ),
    )

    room.components["container"].items.add(lamp.id)
    lamp.components["containable"].parent = room.id

    world.current = room.id
    return world


def test_examine_target_uses_lookable_by_default():
    world = world_with_lookable_item()

    result = world.handle("examine lamp")

    assert result.ok
    assert "brass lamp" in result.message


def test_search_target_does_not_use_lookable_by_default():
    world = world_with_lookable_item()

    result = world.handle("search lamp")

    assert not result.ok
    assert "brass lamp" not in result.message