import pytest

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


@pytest.mark.parametrize(
    ("text", "verb", "target", "preposition", "indirect_target"),
    [
        ("put coin in slot", "put", "coin", "in", "slot"),
        ("put book on table", "put", "book", "on", "table"),
        ("unlock door with key", "unlock", "door", "with", "key"),
        ("give coin to guard", "give", "coin", "to", "guard"),
        ("show badge to guard", "show", "badge", "to", "guard"),
        ("ask guard about boat", "ask", "guard", "about", "boat"),
        ("tell guard about boat", "tell", "guard", "about", "boat"),
    ],
)
def test_uniform_zebra_indirect_commands(
    text,
    verb,
    target,
    preposition,
    indirect_target,
):
    action = parse(text)

    assert action.verb == verb
    assert action.target == target
    assert action.preposition == preposition
    assert action.indirect_target == indirect_target