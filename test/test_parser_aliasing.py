from twip.parser import Parser


def parse(text: str):
    return Parser().parse(text)


def test_l_aliases_look():
    action = parse("l")

    assert action.verb == "look"
    assert action.target == None


def test_x_aliases_examine():
    action = parse("x lamp")

    assert action.verb == "examine"
    assert action.target == "lamp"


def test_i_aliases_inventory():
    action = parse("i")

    assert action.verb == "inventory"
    assert action.target == None


def test_z_aliases_wait():
    action = parse("z")

    assert action.verb == "wait"
    assert action.target == None
