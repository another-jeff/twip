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


def test_drop_inventory_item_moves_it_to_current_room():
    world = World()

    room_entity = room(world, "room")
    player_entity = player(world)
    coin_entity = coin(world)

    world.current = room_entity.id
    world.player_id = player_entity.id
    world.contain(player_entity, coin_entity)

    result = world.handle("drop coin")

    assert result.ok
    assert coin_entity.id not in player_entity.component("container").items
    assert coin_entity.id in room_entity.component("container").items
    assert coin_entity.component("containable").parent == room_entity.id