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


def test_inventory_lists_carried_item():
    world = World()

    player_entity = player(world)
    coin_entity = coin(world)

    world.player_id = player_entity.id
    world.contain(player_entity, coin_entity)

    result = world.handle("inventory")

    assert result.ok
    assert "coin" in result.message