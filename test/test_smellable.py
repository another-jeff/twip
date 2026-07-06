# test/test_smellable.py

from assertions import assert_ok_message
from scenario import bs
from twip.extension import Containable, Smellable


def smellable_flower(world):
    return world.add(
        names=("flower",),
        traits=set(),
        components=(
            Containable(),
            Smellable("The flower smells faintly sweet."),
        ),
    )


def test_smell_smellable_room_target_succeeds():
    s = bs().one_room()
    s.put_room(s.room_one, smellable_flower)

    result = s.handle("smell flower")

    assert_ok_message(result, "The flower smells faintly sweet.")


def test_smell_smellable_inventory_target_succeeds():
    s = bs().one_room()
    s.put_inventory(smellable_flower)

    result = s.handle("smell flower")

    assert_ok_message(result, "The flower smells faintly sweet.")