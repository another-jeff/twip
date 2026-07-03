from twip.entity import Entity
from twip.extension import Openable
from twip.world import World


def test_unknown_target_fails_cleanly():
    world = World()
    entity = Entity(
        key="entity_openable",
        name="openable entity",
        aliases={"thing"},
    )
    entity.add_component(Openable())
    world.add(entity)

    result = world.handle("open window")

    assert not result.ok
    assert "window" in result.message