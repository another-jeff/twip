from twip.extension import Containable, Container
from twip.world import World


def room(world: World, name: str):
    return world.add(
        names=(name,),
        traits=set(),
        components=(Container(),),
    )


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
    
    
def coin_with_trait(world: World, trait: str):
    return world.add(
        names=("coin",),
        traits={trait},
        components=(Containable(),),
    )


def test_take_disambiguated_visible_item_moves_only_that_item():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    red_coin = coin_with_trait(world, "red")
    blue_coin = coin_with_trait(world, "blue")

    world.current = room_entity.id
    world.player_id = player_entity.id
    world.contain(room_entity, red_coin)
    world.contain(room_entity, blue_coin)

    result = world.handle("take red coin")

    assert result.ok
    assert red_coin.id not in room_entity.component("container").items
    assert red_coin.id in player_entity.component("container").items
    assert red_coin.component("containable").parent == player_entity.id

    assert blue_coin.id in room_entity.component("container").items
    assert blue_coin.id not in player_entity.component("container").items
    assert blue_coin.component("containable").parent == room_entity.id


def test_take_visible_containable_moves_it_to_player_inventory():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    coin_entity = coin(world)

    world.current = room_entity.id
    world.player_id = player_entity.id
    world.contain(room_entity, coin_entity)

    result = world.handle("take coin")

    assert result.ok
    assert coin_entity.id not in room_entity.component("container").items
    assert coin_entity.id in player_entity.component("container").items
    assert coin_entity.component("containable").parent == player_entity.id
    
    
def test_take_inventory_item_fails_without_mutation():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    coin_entity = coin(world)

    world.current = room_entity.id
    world.player_id = player_entity.id
    world.contain(player_entity, coin_entity)

    result = world.handle("take coin")

    assert not result.ok
    assert coin_entity.id in player_entity.component("container").items
    assert coin_entity.id not in room_entity.component("container").items
    assert coin_entity.component("containable").parent == player_entity.id