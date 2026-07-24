from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


def test_parser_parses_turn_target_on():
    action = parse("turn lamp on")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "on"
    assert action.target_indirect is None


def test_parser_parses_turn_on_target():
    action = parse("turn on lamp")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "on"
    assert action.target_indirect is None


def test_parser_parses_turn_target_off():
    action = parse("turn lamp off")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "off"
    assert action.target_indirect is None


def test_parser_parses_turn_off_target():
    action = parse("turn off lamp")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "off"
    assert action.target_indirect is None


def test_parser_normalizes_switch_to_turn():
    action = parse("switch lamp on")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "on"
    assert action.target_indirect is None


def test_parser_normalizes_prefix_switch_to_turn():
    action = parse("switch off lamp")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "off"
    assert action.target_indirect is None