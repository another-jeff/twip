import pytest

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


@pytest.mark.parametrize(
    ("text", "verb", "target"),
    [
        ("examine mailbox", "examine", "mailbox"),
        ("take coin", "take", "coin"),
        ("drop coin", "drop", "coin"),
        ("open door", "open", "door"),
        ("push button", "push", "button"),
        ("pull rope", "pull", "rope"),
        ("turn dial", "turn", "dial"),
        ("feel wall", "feel", "wall"),
        ("eat pie", "eat", "pie"),
        ("climb tree", "climb", "tree"),
        ("drink water", "drink", "water"),
        ("wave wand", "wave", "wand"),
        ("fill bottle", "fill", "bottle"),
        ("wear hat", "wear", "hat"),
        ("smell flower", "smell", "flower"),
        ("break vase", "break", "vase"),
        ("burn paper", "burn", "paper"),
        ("enter house", "enter", "house"),
        ("search desk", "search", "desk"),
        ("listen", "listen", ""),
        ("jump", "jump", ""),
        ("sleep", "sleep", ""),
        ("pray", "pray", ""),
        ("wake", "wake", ""),
        ("curse", "curse", ""),
        ("undo", "undo", ""),
        ("sing", "sing", ""),
        ("wait", "wait", ""),
        ("again", "again", ""),
        ("help", "help", ""),
        ("about", "about", ""),
        ("info", "info", ""),
    ],
)
def test_uniform_zebra_common_commands(text, verb, target):
    action = parse(text)

    assert action.verb == verb
    assert action.target == target