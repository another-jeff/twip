from twip.world import World


def test_wait_succeeds():
    world = World()

    result = world.handle("wait")

    assert result.ok
    assert "time passes" in result.message.lower()


def test_z_waits():
    world = World()

    result = world.handle("z")

    assert result.ok
    assert "time passes" in result.message.lower()