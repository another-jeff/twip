from scenario import bs

from twip.behavior import Containable, Container


def test_take_containable_but_not_takeable_fails_without_mutation():
    s = bs().one_room().with_player()

    desk = s.world.add(
        names=("desk",),
        behaviors=(Containable(),),
    )
    s.world.contain(s.room_one, desk)

    result = s.handle("take desk")

    assert not result.ok
    assert result.message == "You can't take desk."
    assert desk.id in s.room_one.behavior(Container.kind).items
    assert desk.id not in s.player.behavior(Container.kind).items