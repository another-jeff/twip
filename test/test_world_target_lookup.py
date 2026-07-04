import tt

from twip.extension import Openable
from twip.world import World


def test_unknown_target_fails_cleanly():
    world = World()
    world.add(
        names=(tt.THING,),
        components=(Openable(),),
    )

    result = world.handle("open window")

    assert not result.ok
    assert "window" in result.message