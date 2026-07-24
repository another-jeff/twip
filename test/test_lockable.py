import tt
from twip.behavior import Lockable, LockState, Openable, OpenState
from twip.world import World


def add_openable_lockable(
    world: World,
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
    key_id: str | None = None,
):
    return world.add(
        names=(tt.THING,),
        behaviors=(
            Openable(state=open_state),
            Lockable(state=lock_state, key_id=key_id),
        ),
    )


def test_open_locked_entity_fails():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.LOCKED)

    result = world.handle("open thing")

    assert not result.ok
    assert "locked" in result.message
    assert entity.behavior(Openable.kind).state == OpenState.CLOSED


def test_open_unlocked_entity_succeeds():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.UNLOCKED)

    result = world.handle("open thing")

    assert result.ok
    assert entity.behavior(Openable.kind).state == OpenState.OPEN


def test_unlock_keyed_entity_with_wrong_key_fails():
    world = World()
    key = world.add(names=("key",))
    world.add(names=("wrong key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    result = world.handle("unlock thing with wrong key")

    assert not result.ok
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED
    
    
def test_unlock_keyed_entity_with_correct_key_succeeds():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    result = world.handle("unlock thing with key")

    assert result.ok
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED
    
def test_unlock_keyed_entity_without_key_fails():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    result = world.handle("unlock thing")

    assert not result.ok
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_unlock_keyed_entity_with_unreachable_key_fails():
    world = World()

    room = world.add_room(names=("room",))
    other_room = world.add_room(names=("other room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(other_room, key)

    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )
    world.put(room, entity)

    result = world.handle("unlock thing with key")

    assert not result.ok
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED
    
    
def test_unlock_keyed_entity_with_key_in_room_fails():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(room, key)
    world.put(room, entity)

    result = world.handle("unlock thing with key")

    assert not result.ok
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED