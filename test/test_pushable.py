# test/test_pushable.py

from twip.behavior import Containable
from twip.extensions import load_extension
from twip.world import World
from twip_ext.pushable import Pushable

from assertions import assert_not_ok_contains, assert_ok_message
from helpers import item
from scenario import bs


BUTTON = "button"
ROCK = "rock"
PUSH_MESSAGE = "The button clicks."


def pushable_button(world: World):
    return world.add(
        names=(BUTTON,),
        traits=set(),
        behaviors=(
            Containable(),
            Pushable(PUSH_MESSAGE),
        ),
    )


def plain_rock(world: World):
    return item(world, ROCK)


def test_push_pushable_target_succeeds(restore_verbs):
    load_extension("twip_ext.pushable")

    s = bs().one_room()
    s.put_room(s.room_one, pushable_button)

    result = s.handle("push button")

    assert_ok_message(result, PUSH_MESSAGE)


def test_push_non_pushable_target_fails_cleanly(restore_verbs):
    load_extension("twip_ext.pushable")

    s = bs().one_room()
    s.put_room(s.room_one, plain_rock)

    result = s.handle("push rock")

    assert_not_ok_contains(result, "can't do that")


def test_push_missing_target_asks_what(restore_verbs):
    load_extension("twip_ext.pushable")

    s = bs().one_room()

    result = s.handle("push")

    assert_not_ok_contains(result, "Push what")