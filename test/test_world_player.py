from twip.extension import Container
from twip.world import World


def player(world: World):
    return world.add(
        names=("player",),
        traits=set(),
        components=(Container(),),
    )


def test_world_can_store_player_id():
    world = World()
    player_entity = player(world)

    world.player_id = player_entity.id

    assert world.player_id == player_entity.id


def test_player_inventory_is_an_ordinary_container():
    world = World()
    player_entity = player(world)

    container = player_entity.component("container")

    assert container.items == set()