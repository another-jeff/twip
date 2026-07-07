# test/test_listenable.py

from assertions import assert_ok_message
from scenario import bs
from twip.behavior import Containable, Listenable


def listenable_shell(world):
    return world.add(
        names=("shell",),
        traits=set(),
        behaviors=(
            Containable(),
            Listenable("You hear the faint hush of the sea."),
        ),
    )


def test_listen_current_room_succeeds():
    s = bs().one_room()
    s.room_one.add_behavior(Listenable("Water drips somewhere in the dark."))

    result = s.handle("listen")

    assert_ok_message(result, "Water drips somewhere in the dark.")


def test_listen_listenable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, listenable_shell)

    result = s.handle("listen shell")

    assert_ok_message(result, "You hear the faint hush of the sea.")


def test_listen_listenable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(listenable_shell)

    result = s.handle("listen shell")

    assert_ok_message(result, "You hear the faint hush of the sea.")