# test/test_parser_semantic_boundaries.py

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


def test_look_examine_and_search_remain_distinct_verbs():
    assert parse("look lamp").verb == "look"
    assert parse("examine lamp").verb == "examine"
    assert parse("search lamp").verb == "search"


def test_x_aliases_examine_but_not_look():
    action = parse("x lamp")

    assert action.verb == "examine"
    assert action.verb != "look"
    assert action.target == "lamp"