# test/test_parser_prepositions.py

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


def test_parser_parses_target_indirect():
    action = parse("kick ball at wall")

    assert action.verb == "kick"
    assert action.target == "ball"
    assert action.preposition == "at"
    assert action.target_indirect == "wall"


def test_parser_parses_prefix_preposition():
    action = parse("look under rug")

    assert action.verb == "look"
    assert action.target == "rug"
    assert action.preposition == "under"
    assert action.target_indirect == ""


def test_parser_parses_postfix_preposition():
    action = parse("turn lamp on")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "on"
    assert action.target_indirect == ""


def test_parser_parses_articles_around_target_indirect():
    action = parse("put the coin in the box")

    assert action.verb == "put"
    assert action.target == "coin"
    assert action.preposition == "in"
    assert action.target_indirect == "box"


def test_parser_still_parses_direction_alias_from_direction_module():
    action = parse("ne")

    assert action.verb == "go"
    assert action.target == "northeast"