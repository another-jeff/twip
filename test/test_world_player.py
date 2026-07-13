from twip.world import World


def player(world: World):
    return world.add(
        names=("player",),
        traits=set(),
    )


def test_world_can_store_player_id():
    world = World()
    player_entity = player(world)

    world.player_id = player_entity.id

    assert world.player_id == player_entity.id


def test_player_can_hold_inventory_without_container_behavior():
    world = World()
    player_entity = player(world)
    world.player_id = player_entity.id

    coin = world.add(names=("coin",))

    world.put(player_entity, coin)

    assert world.contents_of(player_entity) == [coin]
    assert coin.parent == player_entity.id