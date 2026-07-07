# test/test_parser_shapes.py

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


def test_parses_verb_only():
    action = parse("look")

    assert action.verb == "look"
    assert action.target is None
    assert action.preposition is None
    assert action.target_indirect is None


def test_parses_verb_target():
    action = parse("open mailbox")

    assert action.verb == "open"
    assert action.target == "mailbox"
    assert action.preposition is None
    assert action.target_indirect is None


def test_parses_verb_target_preposition_target():
    action = parse("put coin in slot")

    assert action.verb == "put"
    assert action.target == "coin"
    assert action.preposition == "in"
    assert action.target_indirect == "slot"


def test_parses_multiword_target_preposition_target():
    action = parse("unlock front door with brass key")

    assert action.verb == "unlock"
    assert action.target == "front door"
    assert action.preposition == "with"
    assert action.target_indirect == "brass key"


def test_parses_verb_preposition_target():
    action = parse("look under rug")

    assert action.verb == "look"
    assert action.target == "rug"
    assert action.preposition == "under"
    assert action.target_indirect is None
    

def test_parse_verb_preposition_target_command():
    action = parse("look through window")

    assert action.verb == "look"
    assert action.target == "window"
    assert action.preposition == "through"
    assert action.target_indirect is None