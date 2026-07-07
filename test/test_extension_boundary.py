from fake_extension import knockable as extension_knockable
from helpers import item
from scenario import bs
from twip.extensions import load_extension
from twip.verb import VERBS

Knockable = extension_knockable.Knockable


def knockable_door(world):
    door = item(world, "door")
    door.add_behavior(Knockable())
    return door


def test_external_module_loads_registers_verb_and_handles_targeted_action():
    try:
        load_extension(extension_knockable)

        s = bs().one_room()
        s.put_room(s.room_one, knockable_door)

        result = s.handle("knock door")

        assert result.ok
        assert result.message == "You knock on it."
    finally:
        VERBS.pop("knock", None)