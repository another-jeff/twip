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


def test_world_uses_injected_language():
    s = bs().one_room().with_player()
    s.world.language = MarkedEnglish()
    s.put_room(s.room_one, coin)

    result = s.handle("take coin")

    assert_ok_message(result, "take:coin:from:none")