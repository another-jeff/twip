from twip.action import Action
from twip.entity import Entity
from twip.extension import Lookable
from twip.world import World


def test_lookable_describes_entity():
    entity = Entity(
        names=("coin",),
        traits=set(),
        components={},
    )

    lookable = Lookable("A dull copper coin.")

    result = lookable.handle(
        Action(verb="look", target="coin", text="look coin"),
        entity,
        World(),
    )

    assert result.ok
    assert result.message == "A dull copper coin."