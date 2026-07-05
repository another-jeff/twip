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

def statue(world: World):
    return world.add(
        names=("statue",),
        traits=set(),
        components=(),
    )


def test_take_visible_non_containable_fails_without_mutation():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    statue_entity = statue(world)

    world.current = room_entity.id
    world.player_id = player_entity.id

    result = world.handle("take statue")

    assert not result.ok
    assert statue_entity.id not in player_entity.component("container").items


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


def test_take_without_player_fails_without_mutation():
    world = World()

    room_entity = room(world, "room")
    coin_entity = coin(world)

    world.current = room_entity.id
    world.contain(room_entity, coin_entity)

    result = world.handle("take coin")

    assert not result.ok
    assert coin_entity.id in room_entity.component("container").items
    assert coin_entity.component("containable").parent == room_entity.id
    
    
def test_take_same_named_item_in_other_room_does_not_create_ambiguity():
    world = World()

    current_room = room(world, "current-room")
    other_room = room(world, "other-room")
    player_entity = player(world)
    visible_coin = coin(world)
    hidden_coin = coin(world)

    world.current = current_room.id
    world.player_id = player_entity.id
    world.contain(current_room, visible_coin)
    world.contain(other_room, hidden_coin)

    result = world.handle("take coin")

    assert result.ok

    assert visible_coin.id not in current_room.component("container").items
    assert visible_coin.id in player_entity.component("container").items
    assert visible_coin.component("containable").parent == player_entity.id

    assert hidden_coin.id in other_room.component("container").items
    assert hidden_coin.id not in player_entity.component("container").items
    assert hidden_coin.component("containable").parent == other_room.id
    
    
def test_take_ignores_same_named_inventory_item_after_prior_take():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    red_coin = coin_with_trait(world, "red")
    blue_coin = coin_with_trait(world, "blue")

    world.current = room_entity.id
    world.player_id = player_entity.id
    world.contain(room_entity, red_coin)
    world.contain(room_entity, blue_coin)

    first_result = world.handle("take red coin")
    second_result = world.handle("take coin")

    assert first_result.ok
    assert second_result.ok

    assert red_coin.id in player_entity.component("container").items
    assert blue_coin.id in player_entity.component("container").items
    assert red_coin.component("containable").parent == player_entity.id
    assert blue_coin.component("containable").parent == player_entity.id