# test/test_world_examine.py

from twip.entity import Entity
from twip.world import World

from helpers import lookable_item
from scenario import bs


LAMP = "lamp"
LAMP_DESCRIPTION = "A brass lamp with a green shade."


def lamp(world: World) -> Entity:
    return lookable_item(world, LAMP, LAMP_DESCRIPTION)


def scenario():
    s = bs().one_room()
    s.put_room(s.room_one, lamp)
    return s


def test_examine_target_uses_lookable_by_default():
    s = scenario()

    result = s.handle("examine lamp")

    assert result.ok
    assert "brass lamp" in result.message


def test_x_aliases_examine_and_lookable_claims_it():
    s = scenario()

    result = s.handle("x lamp")

    assert result.ok
    assert "brass lamp" in result.message


def test_search_target_does_not_use_lookable_by_default():
    s = scenario()

    result = s.handle("search lamp")

    assert not result.ok
    assert "brass lamp" not in result.message