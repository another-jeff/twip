from collections.abc import Callable

import pytest

from example.prototype import run
from twip.behavior.switchable import Switchable


@pytest.fixture
def prototype_script() -> tuple[Callable[[str], str], list[str]]:
    responses = iter(
        (
            "north",
            "take key",
            "unlock box with key",
            "open box",
            "turn on lamp",
            "wait",
            "look in box",
            "take coin",
            "inventory",
            "put coin in box",
            "look in box",
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
        "You take the key.",
        "Unlocked.",
        "You open the box.",
        "You turn on the lamp.",
        "Time passes.",
        "Inside the box, you see a coin.",
        "You take the coin from the box.",
        "You are carrying a coin and a key.",
        "You put the coin in the box.",
        "Inside the box, you see a coin.",
        "You are carrying a key.",
    ]

    assert world.player_id is not None

    player = world.entity(world.player_id)

    coin = next(
        entity
        for entity in world.entities.values()
        if entity.name == "coin"
    )
    box = next(
        entity
        for entity in world.entities.values()
        if entity.name == "box"
    )
    lamp = next(
        entity
        for entity in world.entities.values()
        if entity.name == "lamp"
    )

    assert lamp.behavior(Switchable.kind).is_on
    assert world.turn == 1

    assert coin not in world.contents_of(player)
    assert coin in world.contents_of(box)
    assert coin.parent == box.id