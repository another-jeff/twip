from twip.behavior import Wearable, WearState
from twip.result import Result

from scenario import bs


def test_wear_carried_wearable_entity():
    s = bs().one_room().with_player()

    hat = s.world.add(
        names=("hat",),
        behaviors=(
            Wearable(),
        ),
    )
    s.world.put(s.player, hat)

    result = s.handle("wear hat")

    assert result == Result.success(
        "You wear the hat.",
        consumes_turn=True,
    )
    assert (
        hat.behavior(Wearable.kind).state
        == WearState.WORN
    )