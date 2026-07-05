# test_world_look.py

from twip.extension import Container, Containable, Lookable
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

    
def test_look_includes_current_room_lookable_text():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(
            Container(),
            Lookable("A round stone chamber."),
        ),
    )

    world.current = room.id

    result = world.handle("look")

    assert result.ok
    assert "rotunda" in result.message
    assert "A round stone chamber." in result.message


def test_look_target_describes_visible_lookable_entity():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    coin = world.add(
        names=("coin",),
        traits=set(),
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    room.components["container"].items.add(coin.id)
    coin.components["containable"].parent = room.id

    world.current = room.id

    result = world.handle("look coin")

    assert result.ok
    assert result.message == "A dull copper coin."
    
    
def test_look_target_ignores_lookable_entity_in_other_room():
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
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    library.components["container"].items.add(coin.id)
    coin.components["containable"].parent = library.id

    world.current = rotunda.id

    result = world.handle("look coin")

    assert not result.ok
    assert "coin" in result.message
    
    
def test_look_target_ambiguity_fails_cleanly():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    copper_coin = world.add(
        names=("coin",),
        traits={"copper"},
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    silver_coin = world.add(
        names=("coin",),
        traits={"silver"},
        components=(
            Containable(),
            Lookable("A bright silver coin."),
        ),
    )

    room.components["container"].items.add(copper_coin.id)
    copper_coin.components["containable"].parent = room.id

    room.components["container"].items.add(silver_coin.id)
    silver_coin.components["containable"].parent = room.id

    world.current = room.id

    result = world.handle("look coin")

    assert not result.ok
    assert "Which coin" in result.message
    
    
def test_look_target_disambiguation_describes_selected_entity():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    copper_coin = world.add(
        names=("coin",),
        traits={"copper"},
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    silver_coin = world.add(
        names=("coin",),
        traits={"silver"},
        components=(
            Containable(),
            Lookable("A bright silver coin."),
        ),
    )

    room.components["container"].items.add(copper_coin.id)
    copper_coin.components["containable"].parent = room.id

    room.components["container"].items.add(silver_coin.id)
    silver_coin.components["containable"].parent = room.id

    world.current = room.id

    result = world.handle("look silver coin")

    assert result.ok
    assert result.message == "A bright silver coin."
    
    
def test_look_target_visible_non_lookable_fails_cleanly():
    world = World()

    room = world.add(
        names=("room", "rotunda"),
        traits={"room"},
        components=(Container(),),
    )

    rock = world.add(
        names=("rock",),
        traits=set(),
        components=(Containable(),),
    )

    room.components["container"].items.add(rock.id)
    rock.components["containable"].parent = room.id

    world.current = room.id

    result = world.handle("look rock")

    assert not result.ok
    assert "can't do that" in result.message
    
    
def test_look_target_can_describe_inventory_item():
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
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    player.components["container"].items.add(coin.id)
    coin.components["containable"].parent = player.id

    world.current = room.id
    world.player_id = player.id

    result = world.handle("look coin")

    assert result.ok
    assert result.message == "A dull copper coin."
    
    
def test_look_target_ambiguity_includes_room_and_inventory_items():
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

    room_coin = world.add(
        names=("coin",),
        traits={"copper"},
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    inventory_coin = world.add(
        names=("coin",),
        traits={"silver"},
        components=(
            Containable(),
            Lookable("A bright silver coin."),
        ),
    )

    room.components["container"].items.add(room_coin.id)
    room_coin.components["containable"].parent = room.id

    player.components["container"].items.add(inventory_coin.id)
    inventory_coin.components["containable"].parent = player.id

    world.current = room.id
    world.player_id = player.id

    result = world.handle("look coin")

    assert not result.ok
    assert "Which coin" in result.message
    
    
def test_look_target_disambiguation_selects_inventory_item_over_room_item():
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

    room_coin = world.add(
        names=("coin",),
        traits={"copper"},
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    inventory_coin = world.add(
        names=("coin",),
        traits={"silver"},
        components=(
            Containable(),
            Lookable("A bright silver coin."),
        ),
    )

    room.components["container"].items.add(room_coin.id)
    room_coin.components["containable"].parent = room.id

    player.components["container"].items.add(inventory_coin.id)
    inventory_coin.components["containable"].parent = player.id

    world.current = room.id
    world.player_id = player.id

    result = world.handle("look silver coin")

    assert result.ok
    assert result.message == "A bright silver coin."
    
    
def test_look_target_disambiguation_selects_room_item_over_inventory_item():
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

    room_coin = world.add(
        names=("coin",),
        traits={"copper"},
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    inventory_coin = world.add(
        names=("coin",),
        traits={"silver"},
        components=(
            Containable(),
            Lookable("A bright silver coin."),
        ),
    )

    room.components["container"].items.add(room_coin.id)
    room_coin.components["containable"].parent = room.id

    player.components["container"].items.add(inventory_coin.id)
    inventory_coin.components["containable"].parent = player.id

    world.current = room.id
    world.player_id = player.id

    result = world.handle("look copper coin")

    assert result.ok
    assert result.message == "A dull copper coin."


def test_look_target_inventory_non_lookable_fails_cleanly():
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

    rock = world.add(
        names=("rock",),
        traits=set(),
        components=(Containable(),),
    )

    player.components["container"].items.add(rock.id)
    rock.components["containable"].parent = player.id

    world.current = room.id
    world.player_id = player.id

    result = world.handle("look rock")

    assert not result.ok
    assert "can't do that" in result.message
    
    
def test_look_target_inventory_item_ignores_same_named_item_in_other_room():
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

    player = world.add(
        names=("player",),
        traits={"player"},
        components=(Container(),),
    )

    library_coin = world.add(
        names=("coin",),
        traits={"copper"},
        components=(
            Containable(),
            Lookable("A dull copper coin."),
        ),
    )

    inventory_coin = world.add(
        names=("coin",),
        traits={"silver"},
        components=(
            Containable(),
            Lookable("A bright silver coin."),
        ),
    )

    library.components["container"].items.add(library_coin.id)
    library_coin.components["containable"].parent = library.id

    player.components["container"].items.add(inventory_coin.id)
    inventory_coin.components["containable"].parent = player.id

    world.current = rotunda.id
    world.player_id = player.id

    result = world.handle("look coin")

    assert result.ok
    assert result.message == "A bright silver coin."