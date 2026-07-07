from helpers import item
from scenario import bs
from twip.extension_loader import load_extension
from twip.verb import VERBS


def test_external_module_loads_from_import_path_and_handles_targeted_action():
    try:
        extension_knockable = load_extension("fake_extension.knockable")
        Knockable = extension_knockable.Knockable

        def knockable_door(world):
            door = item(world, "door")
            door.add_behavior(Knockable())
            return door

        s = bs().one_room()
        s.put_room(s.room_one, knockable_door)

        result = s.handle("knock door")

        assert result.ok
        assert result.message == "You knock on it."
    finally:
        VERBS.pop("knock", None)