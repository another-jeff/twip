from collections.abc import Callable

import pytest

from example.prototype import run


@pytest.fixture
def prototype_script() -> tuple[Callable[[str], str], list[str]]:
    responses = iter(
        (
            "north",
            "open box",
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
        "You open the box.",
        "Inside the box, you see a coin.",
        "You take the coin from the box.",
        "You are carrying a coin.",
        "You put the coin in the box.",
        "Inside the box, you see a coin.",
        "You are carrying nothing.",
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

    assert coin not in world.contents_of(player)
    assert coin in world.contents_of(box)
    assert coin.parent == box.id