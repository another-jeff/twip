from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.behavior import Behavior
from twip.result import Result
from twip.verb import VERBS, register_verb


def test_external_style_behavior_registers_verb_and_handles_targeted_action():
    try:
        register_verb("knock")

        s = bs().one_room()
        s.put_room(s.room_one, knockable_door)

        result = s.handle("knock door")

        assert result.ok
        assert result.message == "You knock on it."
    finally:
        VERBS.pop("knock", None)

from helpers import item
from scenario import bs


@dataclass
class Knockable(Behavior):
    kind: ClassVar[str] = "knockable"

    def handle(self, action: Action, entity, world) -> Result | None:
        if action.verb != "knock":
            return None

        return Result.success("You knock on it.")


def knockable_door(world):
    door = item(world, "door")
    door.add_behavior(Knockable())
    return door


def test_external_style_behavior_handles_targeted_action_without_dispatcher_change():
    s = bs().one_room()
    s.put_room(s.room_one, knockable_door)

    result = s.handle("knock door")

    assert result.ok
    assert result.message == "You knock on it."
    

def test_external_style_behavior_registers_verb_and_handles_targeted_action():
    try:
        register_verb("knock")

        s = bs().one_room()
        s.put_room(s.room_one, knockable_door)

        result = s.handle("knock door")

        assert result.ok
        assert result.message == "You knock on it."
    finally:
        VERBS.pop("knock", None)