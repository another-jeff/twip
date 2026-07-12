# example/prototype.py

from twip import direction
from twip.behavior import (
    Containable,
    Container,
    Lookable,
    Openable,
    Takeable,
)
from twip.play import play
from twip.world import World


def build_world() -> World:
    world = World()

    porch = world.add(
        names=("room", "front porch"),
        behaviors=(
            Container(),
            Lookable(
                "A narrow porch faces a quiet road. "
                "The entry hall lies to the north."
            ),
        ),
    )

    hall = world.add(
        names=("room", "entry hall"),
        behaviors=(
            Container(),
            Lookable(
                "A small, mostly empty hall. "
                "The front porch lies to the south."
            ),
        ),
    )
    
    desk = world.add(
        names=("desk", "writing desk"),
        behaviors=(
            Containable(),
            Lookable(
                "A narrow writing desk with a scarred wooden surface."
            ),
        ),
    )
    world.contain(hall, desk)

    world.add_and_connect(
        names=("doorway",),
        connections=(
            (porch, direction.N),
            (hall, direction.S),
        ),
    )
    
    box = world.add(
        names=("box", "wooden box"),
        behaviors=(
            Containable(),
            Container(),
            Openable(),
            Lookable("A squat wooden box with a hinged lid."),
        ),
    )
    world.contain(hall, box)
    
    coin = world.add(
        names=("coin", "brass coin"),
        behaviors=(
            Containable(),
            Takeable(),
            Lookable("A dull brass coin, worn nearly smooth."),
        ),
    )
    world.contain(box, coin)

    player = world.add(
        names=("player",),
        behaviors=(Container(),),
    )
    world.player_id = player.id

    world.current = porch.id
    
    return world


def main() -> None:
    world = build_world()

    print("Twip Prototype")
    print()
    print(world.handle("look").message)

    play(world)


if __name__ == "__main__":
    main()