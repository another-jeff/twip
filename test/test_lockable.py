import tt

from twip.behavior import Container, Lockable, LockState, Openable, OpenState
from twip.result import Result
from twip.world import World


def add_openable_lockable(
    world: World,
    *,
    open_state: OpenState = OpenState.CLOSED,
    lock_state: LockState = LockState.LOCKED,
    key_id: str | None = None,
    key_required_to_lock: bool = True,
    key_required_to_unlock: bool = True,
):
    return world.add(
        names=(tt.THING,),
        behaviors=(
            Openable(state=open_state),
            Lockable(
                state=lock_state,
                key_id=key_id,
                key_required_to_lock=key_required_to_lock,
                key_required_to_unlock=key_required_to_unlock,
            ),
        ),
    )


def test_open_locked_entity_fails():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.LOCKED)

    result = world.handle("open thing")

    assert result == Result.failure("The thing is locked.")
    assert entity.behavior(Openable.kind).state == OpenState.CLOSED


def test_open_unlocked_entity_succeeds():
    world = World()
    entity = add_openable_lockable(world, lock_state=LockState.UNLOCKED)

    result = world.handle("open thing")

    assert result == Result.success("You open the thing.")
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

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_unlock_keyed_entity_with_correct_key_succeeds():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    result = world.handle("unlock thing with key")

    assert result == Result.success("Unlocked.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED


def test_unlock_keyed_entity_without_key_fails():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    result = world.handle("unlock thing")

    assert result == Result.failure("That key doesn't fit.")
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

    assert result == Result.failure("That key doesn't fit.")
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

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_unlock_keyed_entity_with_key_in_closed_carried_container_fails():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    container = world.add(
        names=("box",),
        behaviors=(
            Openable(state=OpenState.CLOSED),
            Container(),
        ),
    )
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, container)
    world.put(container, key)
    world.put(room, entity)

    result = world.handle("unlock thing with key")

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_unlock_keyed_entity_with_correct_carried_key_and_wrong_key_succeeds():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    wrong_key = world.add(names=("wrong key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, key)
    world.put(player, wrong_key)
    world.put(room, entity)

    result = world.handle("unlock thing with key")

    assert result == Result.success("Unlocked.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED


def test_unlock_keyed_entity_then_open_succeeds():
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
    world.put(player, key)
    world.put(room, entity)

    unlock_result = world.handle("unlock thing with key")
    open_result = world.handle("open thing")

    assert unlock_result == Result.success("Unlocked.")
    assert open_result == Result.success("You open the thing.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED
    assert entity.behavior(Openable.kind).state == OpenState.OPEN


def test_lock_keyed_entity_without_key_fails():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
    )

    result = world.handle("lock thing")

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED


def test_lock_keyed_entity_with_correct_carried_key_succeeds():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, key)
    world.put(room, entity)

    result = world.handle("lock thing with key")

    assert result == Result.success("Locked.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_lock_keyed_entity_with_wrong_carried_key_fails():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    wrong_key = world.add(names=("wrong key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, wrong_key)
    world.put(room, entity)

    result = world.handle("lock thing with wrong key")

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED


def test_lock_keyed_entity_without_key_succeeds_when_key_not_required():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
        key_required_to_lock=False,
    )

    result = world.handle("lock thing")

    assert result == Result.success("Locked.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_unlock_keyed_entity_without_key_succeeds_when_key_not_required():
    world = World()
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        key_id=key.id,
        key_required_to_unlock=False,
    )

    result = world.handle("unlock thing")

    assert result == Result.success("Unlocked.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED


def test_unlock_keyed_entity_with_invalid_preposition_fails():
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
    world.put(player, key)
    world.put(room, entity)

    result = world.handle("unlock thing in key")

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_lock_keyed_entity_with_invalid_preposition_fails():
    world = World()

    room = world.add_room(names=("room",))
    player = world.add(names=("player",))
    key = world.add(names=("key",))
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=key.id,
    )

    world.current = room.id
    world.player_id = player.id
    world.put(room, player)
    world.put(player, key)
    world.put(room, entity)

    result = world.handle("lock thing in key")

    assert result == Result.failure("That key doesn't fit.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED


def test_lock_already_locked_entity_fails():
    world = World()
    entity = add_openable_lockable(
        world,
        lock_state=LockState.LOCKED,
        key_id=None,
    )

    result = world.handle("lock thing")

    assert result == Result.failure("It's already locked.")
    assert entity.behavior(Lockable.kind).state == LockState.LOCKED


def test_unlock_already_unlocked_entity_fails():
    world = World()
    entity = add_openable_lockable(
        world,
        lock_state=LockState.UNLOCKED,
        key_id=None,
    )

    result = world.handle("unlock thing")

    assert result == Result.failure("It's already unlocked.")
    assert entity.behavior(Lockable.kind).state == LockState.UNLOCKED