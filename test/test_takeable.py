from assertions import assert_contains, assert_does_not_contain
from scenario import bs


def test_take_non_takeable_fails_without_mutation():
    s = bs().one_room().with_player()

    desk = s.world.add(names=("desk",))
    s.world.put(s.room_one, desk)

    result = s.handle("take desk")

    assert not result.ok
    assert result.message == "You can't take the desk."
    assert_contains(s.room_one, desk)
    assert_does_not_contain(s.player, desk)