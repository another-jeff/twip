from twip.entity import Entity
from twip.language import English

from assertions import assert_ok_message
from helpers import coin
from scenario import bs


class MarkedEnglish(English):
    def take_success(
        self,
        item: Entity,
        source: Entity | None,
    ) -> str:
        source_name = source.name if source else "none"
        return f"take:{item.name}:from:{source_name}"


class MovementEnglish(English):
    def movement_success(self, direction: str) -> str:
        return f"move:{direction}"



def test_world_uses_injected_language():
    s = bs().one_room().with_player()
    s.world.language = MarkedEnglish()
    s.put_room(s.room_one, coin)

    result = s.handle("take coin")

    assert_ok_message(result, "take:coin:from:none")
    


def test_world_uses_injected_language_for_movement():
    s = bs().two_rooms()
    s.world.language = MovementEnglish()
    s.connect()

    result = s.handle("go north")

    assert_ok_message(result, "move:north")