# test_world_look.py

from twip.extension import Container, Containable
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


def test_look_lists_current_room_contents():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    coin = world.add(
        names=("coin",),
        traits=set(),
        components=(Containable(),),
    )

    room.components["container"].items.add(coin.id)
    coin.components["containable"].parent = room.id
    world.current = room.id

    result = world.handle("look")

    assert result.ok
    assert "rotunda" in result.message
    assert "coin" in result.message
    
    
def test_look_lists_only_current_room_contents():
    world = World()

    rotunda = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    library = world.add(
        names=("room", "library"),
        traits={"room"},
        components=(Container(),),
    )

    coin = world.add(
        names=("coin",),
        traits=set(),
        components=(Containable(),),
    )

    gem = world.add(
        names=("gem",),
        traits=set(),
        components=(Containable(),),
    )

    rotunda.components["container"].items.add(coin.id)
    coin.components["containable"].parent = rotunda.id

    library.components["container"].items.add(gem.id)
    gem.components["containable"].parent = library.id

    world.current = rotunda.id

    result = world.handle("look")

    assert result.ok
    assert "rotunda" in result.message
    assert "coin" in result.message
    assert "gem" not in result.message
    
    
def test_look_does_not_list_inventory_contents():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    player = world.add(
        names=("player",),
        traits={"player"},
        components=(Container(),),
    )

    coin = world.add(
        names=("coin",),
        traits=set(),
        components=(Containable(),),
    )

    player.components["container"].items.add(coin.id)
    coin.components["containable"].parent = player.id

    world.current = room.id
    world.player_id = player.id

    result = world.handle("look")

    assert result.ok
    assert "rotunda" in result.message
    assert "coin" not in result.message
    
    
def test_look_lists_multiple_current_room_contents():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    coin = world.add(
        names=("coin",),
        traits=set(),
        components=(Containable(),),
    )

    key = world.add(
        names=("key",),
        traits=set(),
        components=(Containable(),),
    )

    room.components["container"].items.add(coin.id)
    coin.components["containable"].parent = room.id

    room.components["container"].items.add(key.id)
    key.components["containable"].parent = room.id

    world.current = room.id

    result = world.handle("look")

    assert result.ok
    assert "rotunda" in result.message
    assert "coin" in result.message
    assert "key" in result.message


def test_look_lists_room_contents_in_name_order():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    zebra = world.add(
        names=("zebra",),
        traits=set(),
        components=(Containable(),),
    )

    apple = world.add(
        names=("apple",),
        traits=set(),
        components=(Containable(),),
    )

    room.components["container"].items.add(zebra.id)
    zebra.components["containable"].parent = room.id

    room.components["container"].items.add(apple.id)
    apple.components["containable"].parent = room.id

    world.current = room.id

    result = world.handle("look")

    assert result.ok
    assert result.message.index("apple") < result.message.index("zebra")