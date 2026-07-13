# test/test_pullable.py

from twip.behavior import Pullable
from twip.world import World

from assertions import assert_not_ok_contains, assert_ok_message
from helpers import item
from scenario import bs


LEVER = "lever"
ROCK = "rock"
PULL_MESSAGE = "The lever moves."


def pullable_lever(world: World):
    return world.add(
        names=(LEVER,),
        traits=set(),
        behaviors=(
            Pullable(PULL_MESSAGE),
        ),
    )


def plain_rock(world: World):
    return item(world, ROCK)


def test_pull_pullable_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, pullable_lever)

    result = s.handle("pull lever")

    assert_ok_message(result, PULL_MESSAGE)


def test_pull_non_pullable_target_fails_cleanly():
    s = bs().one_room()
    s.put_room(s.room_one, plain_rock)

    result = s.handle("pull rock")

    assert_not_ok_contains(result, "can't do that")


def test_pull_missing_target_asks_what():
    s = bs().one_room()

    result = s.handle("pull")

    assert_not_ok_contains(result, "Pull what")