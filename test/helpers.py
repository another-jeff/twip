from twip.entity import Entity
from twip.behavior import Container, Lookable, Takeable
from twip.world import World

import tt

def room(world: World, trait: str) -> Entity:
    return world.add(
        names=(tt.ROOM,),
        traits={trait},
        behaviors=(Container(),),
    )


def named_room(world: World, name: str) -> Entity:
    return world.add(
        names=(tt.ROOM, name),
        traits=set(),
        behaviors=(Container(),),
    )


def described_room(world: World, name: str = tt.ROTUNDA) -> Entity:
    return world.add(
        names=(tt.ROOM, name),
        traits=set(),
        behaviors=(
            Container(),
            Lookable(tt.ROOM_DESCRIPTION),
        ),
    )


def player(world: World) -> Entity:
    return world.add(
        names=(tt.PLAYER,),
        traits=set(),
        behaviors=(Container(),),
    )


def item(world: World, name: str) -> Entity:
    return world.add(
        names=(name,),
        traits=set(),
        behaviors=(
            Takeable(),
        ),
    )


def item_with_trait(world: World, name: str, trait: str) -> Entity:
    return world.add(
        names=(name,),
        traits={trait},
        behaviors=(
            Takeable(),
        ),
    )


def lookable_item(world: World, name: str, text: str) -> Entity:
    return world.add(
        names=(name,),
        traits=set(),
        behaviors=(
            Lookable(text),
            Takeable(),
        ),
    )


def lookable_item_with_trait(
    world: World,
    name: str,
    trait: str,
    text: str,
) -> Entity:
    return world.add(
        names=(name,),
        traits={trait},
        behaviors=(
            Lookable(text),
            Takeable(),
        ),
    )

def coin(world: World) -> Entity:
    return item(world, tt.COIN)


def coin_red(world: World) -> Entity:
    return item_with_trait(world, tt.COIN, tt.RED)


def coin_blue(world: World) -> Entity:
    return item_with_trait(world, tt.COIN, tt.BLUE)


def coin_copper(world: World) -> Entity:
    return lookable_item_with_trait(
        world,
        tt.COIN,
        tt.COPPER,
        tt.COPPER_COIN_DESCRIPTION,
    )


def coin_silver(world: World) -> Entity:
    return lookable_item_with_trait(
        world,
        tt.COIN,
        tt.SILVER,
        tt.SILVER_COIN_DESCRIPTION,
    )


def statue(world: World) -> Entity:
    return world.add(
        names=(tt.STATUE,),
        traits=set(),
        behaviors=(),
    )