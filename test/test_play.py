# test/test_play.py

from types import SimpleNamespace

import pytest

from twip.play import play


class FakeWorld:
    def __init__(self):
        self.commands = []

    def handle(self, text: str):
        self.commands.append(text)
        return SimpleNamespace(message=f"handled: {text}")


def make_reader(*responses):
    responses = iter(responses)

    def read(_prompt: str) -> str:
        response = next(responses)

        if isinstance(response, BaseException):
            raise response

        return response

    return read


def test_plays_commands_until_quit():
    world = FakeWorld()
    output = []

    play(
        world,
        read=make_reader("look", "north", "quit"),
        write=output.append,
    )

    assert world.commands == ["look", "north"]
    assert output == [
        "handled: look",
        "handled: north",
    ]


def test_ignores_blank_input():
    world = FakeWorld()
    output = []

    play(
        world,
        read=make_reader("", "   ", "look", "exit"),
        write=output.append,
    )

    assert world.commands == ["look"]
    assert output == ["handled: look"]


@pytest.mark.parametrize("exception", [EOFError(), KeyboardInterrupt()])
def test_stops_cleanly_when_input_ends(exception):
    world = FakeWorld()
    output = []

    play(
        world,
        read=make_reader("look", exception),
        write=output.append,
    )

    assert world.commands == ["look"]
    assert output == [
        "handled: look",
        "",
    ]