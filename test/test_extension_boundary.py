from twip.verb import VERBS

from helpers import item
from scenario import bs
from fake_extension.knockable import Knockable, register


def knockable_door(world):
    door = item(world, "door")
    door.add_behavior(Knockable())
    return door


def test_external_module_registers_verb_and_handles_targeted_action():
    try:
        register()

        s = bs().one_room()
        s.put_room(s.room_one, knockable_door)

        result = s.handle("knock door")

        assert result.ok
        assert result.message == "You knock on it."
    finally:
        VERBS.pop("knock", None)
        
        
def test_external_style_behavior_handles_targeted_action_without_dispatcher_change():
    s = bs().one_room()
    s.put_room(s.room_one, knockable_door)

    result = s.handle("knock door")

    assert result.ok
    assert result.message == "You knock on it."