# test/test_parser_indirect.py

from twip.parser import Parser


def test_parser_parses_target_preposition_indirect():
    action = Parser().parse("kick ball at wall")

    assert action.verb == "kick"
    assert action.target == "ball"
    assert action.preposition == "at"
    assert action.target_indirect == "wall"


def test_parser_parses_look_under_target():
    action = Parser().parse("look under rug")

    assert action.verb == "look"
    assert action.target == "rug"
    assert action.preposition == "under"
    assert action.target_indirect == None


def test_parser_parses_put_target_in_indirect():
    action = Parser().parse("put coin in box")

    assert action.verb == "put"
    assert action.target == "coin"
    assert action.preposition == "in"
    assert action.target_indirect == "box"