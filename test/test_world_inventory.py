from twip.extension import Containable, Container
from twip.world import World


def player(world: World):
    return world.add(
        names=("player",),
        traits=set(),
        components=(Container(),),
    )


def coin(world: World):
    return world.add(
        names=("coin",),
        traits=set(),
        components=(Containable(),),
    )

def key(world: World):
    return world.add(
        names=("key",),
        traits=set(),
        components=(Containable(),),
    )
    
def room(world: World, name: str):
    return world.add(
        names=(name,),
        traits=set(),
        components=(Container(),),
    )


def test_inventory_lists_only_carried_items_not_room_items():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    carried_key = key(world)
    room_coin = coin(world)

    world.current = room_entity.id
    world.player_id = player_entity.id
    world.contain(player_entity, carried_key)
    world.contain(room_entity, room_coin)

    result = world.handle("inventory")

    assert result.ok
    assert "key" in result.message
    assert "coin" not in result.message


def test_inventory_lists_multiple_carried_items():
    world = World()

    player_entity = player(world)
    coin_entity = coin(world)
    key_entity = key(world)

    world.player_id = player_entity.id
    world.contain(player_entity, coin_entity)
    world.contain(player_entity, key_entity)

    result = world.handle("inventory")

    assert result.ok
    assert "coin" in result.message
    assert "key" in result.message


def test_inventory_lists_carried_item():
    world = World()

    player_entity = player(world)
    coin_entity = coin(world)

    world.player_id = player_entity.id
    world.contain(player_entity, coin_entity)

    result = world.handle("inventory")

    assert result.ok
    assert "coin" in result.message
    
    
def test_inventory_empty_reports_nothing_carried():
    world = World()

    player_entity = player(world)

    world.player_id = player_entity.id

    result = world.handle("inventory")

    assert result.ok
    assert "nothing" in result.message


def test_inventory_without_player_fails():
    world = World()

    result = world.handle("inventory")

    assert not result.ok
    assert "player" in result.message