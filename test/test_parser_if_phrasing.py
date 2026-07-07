# test/test_parser_if_phrases.py

from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


def test_listen_to_target():
    action = parse("listen to door")

    assert action.verb == "listen"
    assert action.target == "door"
    assert action.preposition == "to"
    assert action.target_indirect == ""


def test_look_under_target():
    action = parse("look under rug")

    assert action.verb == "look"
    assert action.target == "rug"
    assert action.preposition == "under"
    assert action.target_indirect == ""


def test_turn_target_on():
    action = parse("turn lamp on")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "on"
    assert action.target_indirect == ""


def test_turn_on_target():
    action = parse("turn on lamp")

    assert action.verb == "turn"
    assert action.target == "lamp"
    assert action.preposition == "on"
    assert action.target_indirect == ""


def test_take_target_off():
    action = parse("take hat off")

    assert action.verb == "take"
    assert action.target == "hat"
    assert action.preposition == "off"
    assert action.target_indirect == ""


def test_take_off_target():
    action = parse("take off hat")

    assert action.verb == "take"
    assert action.target == "hat"
    assert action.preposition == "off"
    assert action.target_indirect == ""


def test_wake_up_is_phrase_verb():
    action = parse("wake up")

    assert action.verb == "wake"
    assert action.target == ""
    assert action.preposition == "up"
    assert action.target_indirect == ""


def test_talk_to_target():
    action = parse("talk to guard")

    assert action.verb == "talk"
    assert action.target == "guard"
    assert action.preposition == "to"
    assert action.target_indirect == ""
    

def test_dig_in_target():
    action = parse("dig in dirt")

    assert action.verb == "dig"
    assert action.target == "dirt"
    assert action.preposition == "in"
    assert action.target_indirect == ""