# test_world_look.py

from twip.extension import Container
from twip.world import World


def test_look_describes_current_room():
    world = World()
    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )
    world.current = room.id

    result = world.handle("look")

    assert result.ok
    assert "rotunda" in result.message


def test_look_without_current_room_fails_cleanly():
    world = World()

    result = world.handle("look")

    assert not result.ok
    assert "nowhere" in result.message.lower() or "current" in result.message.lower()
