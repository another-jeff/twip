import pytest

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


@pytest.mark.parametrize(
    ("text", "direction"),
    [
        ("n", "north"),
        ("e", "east"),
        ("s", "south"),
        ("w", "west"),
        ("ne", "northeast"),
        ("se", "southeast"),
        ("nw", "northwest"),
        ("sw", "southwest"),
        ("u", "up"),
        ("up", "up"),
        ("d", "down"),
        ("down", "down"),
        ("in", "in"),
        ("out", "out"),
    ],
)
def test_direction_aliases_go_direction(text: str, direction: str):
    action = parse(text)

    assert action.verb == "go"
    assert action.target == direction