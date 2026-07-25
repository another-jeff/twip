from collections.abc import Callable

from twip import direction
from twip.behavior import (
    Container,
    Lockable,
    Lookable,
    Openable,
    Switchable,
    Takeable,
)
from twip.behavior.lockable import LockState
from twip.play import play
from twip.world import World


def build_world() -> World:
    world = World()

    porch = world.add(
        names=("room", "Front Porch"),
        behaviors=(
            Container(),
            Lookable(
                "A narrow porch faces a quiet road. "
                "The entry hall lies to the north."
            ),
        ),
    )

    hall = world.add(
        names=("room", "Entry Hall"),
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
            Lookable(
                "A narrow writing desk with a scarred wooden surface."
            ),
        ),
    )
    world.put(hall, desk)

    world.add_and_connect(
        names=("doorway",),
        connections=(
            (porch, direction.N),
            (hall, direction.S),
        ),
    )

    key = world.add(
        names=("key", "small key"),
        behaviors=(
            Takeable(),
            Lookable("A small iron key."),
        ),
    )
    world.put(hall, key)

    lamp = world.add(
        names=("lamp",),
        behaviors=(
            Switchable(),
            Lookable("A plain electric lamp."),
        ),
    )
    world.put(hall, lamp)

    box = world.add(
        names=("box", "wooden box"),
        behaviors=(
            Container(),
            Openable(),
            Lockable(
                state=LockState.LOCKED,
                key_id=key.id,
            ),
            Lookable("A squat wooden box with a hinged lid."),
        ),
    )
    world.put(hall, box)

    coin = world.add(
        names=("coin", "brass coin"),
        behaviors=(
            Takeable(),
            Lookable("A dull brass coin, worn nearly smooth."),
        ),
    )
    world.put(box, coin)

    player = world.add(
        names=("player",),
        behaviors=(Container(),),
    )
    world.player_id = player.id
    world.current = porch.id

    return world


def run(
    *,
    read: Callable[[str], str] = input,
    write: Callable[[str], None] = print,
) -> World:
    world = build_world()

    write("Twip Prototype")
    write("")
    write(world.handle("look").message)

    play(world, read=read, write=write)

    return world


def main() -> None:
    run()


if __name__ == "__main__":
    main()