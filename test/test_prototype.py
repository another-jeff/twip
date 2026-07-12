from collections.abc import Callable

import pytest

from example.prototype import run
from twip.behavior import Containable, Container


@pytest.fixture
def prototype_script() -> tuple[Callable[[str], str], list[str]]:
    responses = iter(
        (
            "north",
            "open box",
            "look in box",
            "take coin",
            "inventory",
            "quit",
        )
    )
    output: list[str] = []

    def read(_prompt: str) -> str:
        return next(responses)

    return read, output


def test_prototype_script(
    prototype_script: tuple[Callable[[str], str], list[str]],
):
    read, output = prototype_script

    world = run(read=read, write=output.append)

    assert output == [
        "Twip Prototype",
        "",
        (
            "Front Porch\n"
            "A narrow porch faces a quiet road. "
            "The entry hall lies to the north."
        ),
        "You go north.",
        "You open the box.",
        "Inside the box, you see a coin.",
        "You take the coin from the box.",
        "You are carrying a coin.",
    ]

    assert world.player_id is not None
    player = world.entity(world.player_id)
    inventory = player.behavior(Container.kind)
    assert isinstance(inventory, Container)

    coin = next(
        entity
        for entity in world.entities.values()
        if entity.name == "coin"
    )
    containable = coin.behavior(Containable.kind)
    assert isinstance(containable, Containable)

    assert coin.id in inventory.items
    assert containable.parent == player.id