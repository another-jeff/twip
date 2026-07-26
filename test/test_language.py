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
    

class MovementEnglish(English):
    def movement_success(self, direction: str) -> str:
        return f"move:{direction}"


def test_world_uses_injected_language_for_movement():
    s = bs().two_rooms()
    s.world.language = MovementEnglish()
    s.connect()

    result = s.handle("go north")

    assert_ok_message(result, "move:north")
    
    
class DropEnglish(English):
    def drop_success(self, item: Entity) -> str:
        return f"drop:{item.name}"


def test_world_uses_injected_language_for_drop():
    s = bs().one_room().with_player()
    coin = s.world.add(names=("coin",))
    s.world.put(s.player, coin)
    s.world.language = DropEnglish()

    result = s.handle("drop coin")

    assert_ok_message(result, "drop:coin")
    
    
class AmbiguousEnglish(English):
    def ambiguous(self, target: str) -> str:
        return f"ambiguous:{target}"


def test_world_uses_injected_language_for_ambiguity():
    s = bs().one_room().with_player()
    s.world.language = AmbiguousEnglish()

    first = s.world.add(names=("coin",))
    second = s.world.add(names=("coin",))

    s.world.put(s.room_one, first)
    s.world.put(s.room_one, second)

    result = s.handle("take coin")

    assert not result.ok
    assert result.message == "ambiguous:coin"
    
    
class WaitEnglish(English):
    def wait_success(self) -> str:
        return "waited"


def test_world_uses_injected_language_for_wait():
    s = bs()
    s.world.language = WaitEnglish()

    result = s.handle("wait")

    assert_ok_message(result, "waited")
    assert result.consumes_turn
    
class DispatcherEnglish(English):
    def nothing_happens(self) -> str:
        return "nothing"

    def missing_target(self, verb: str) -> str:
        return f"missing:{verb}"

    def unsupported_action(self) -> str:
        return "unsupported"


def test_world_uses_injected_language_for_nothing_happens():
    s = bs()
    s.world.language = DispatcherEnglish()

    result = s.handle("sing")

    assert not result.ok
    assert result.message == "nothing"


def test_world_uses_injected_language_for_missing_target():
    s = bs()
    s.world.language = DispatcherEnglish()

    result = s.handle("eat")

    assert not result.ok
    assert result.message == "missing:eat"


def test_world_uses_injected_language_for_unsupported_action():
    s = bs().one_room().with_player()
    s.world.language = DispatcherEnglish()

    rock = s.world.add(names=("rock",))
    s.world.put(s.room_one, rock)

    result = s.handle("eat rock")

    assert not result.ok
    assert result.message == "unsupported"