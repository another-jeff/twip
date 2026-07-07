# Milestone 007: Basic Test Scenarios

Tests now use a shared `BasicScenario` helper for common world setup.

Core test vocabulary:

```python
s = bs().one_room()
s = bs().two_rooms()
s = bs().three_rooms()
s = bs().one_room().with_player()
```

Scenario room labels are intentionally test-facing:

```text
room_one
room_two
room_three
```

Parser-facing room names are ordinary test constants:

```text
tt.ROOM_1
tt.ROOM_2
tt.ROOM_3
```

The helper supports common placement:

```python
s.put_room(s.room_one, coin)
s.put_room(s.room_two, coin, key)
s.put_inventory(coin)
```

And simple default movement setup:

```python
s.connect()
s.connect(s.room_three)
s.connect(traits={tt.WOODEN})
s.connect(behaviors=(Openable(state=OpenState.CLOSED),))
```

`BasicScenario.connect()` is deliberately opinionated:

```text
room_one north -> room_two
room_two south -> room_one
```

or, when given a room:

```text
room_one north -> given room
given room south -> room_one
```

This replaced older local scenario wrappers based on `SimpleNamespace`, custom dataclasses, and many optional setup parameters.

Important distinction preserved:

```text
Visibility:
  room.Container.items determines what is visible in the room

Move/take/drop containment:
  Containable.parent determines whether an entity can be moved between containers
```

So visible objects do not have to be takeable. For example, a statue can be visible in a room without being `Containable`.

The guiding rule for tests is now:

```text
Prefer readable world shape over configurable setup knobs.
```

Tests should say what world exists:

```python
s = bs().two_rooms().with_player()

coin = s.put_room(s.room_one, coin_copper)
gem = s.put_room(s.room_two, coin_silver)
```

rather than encode setup through opaque parameters:

```python
scenario(
    room_item=coin_copper,
    other_room_item=coin_silver,
    inventory_item=coin_gold,
)
```

Current result:

```text
Test setup is more explicit.
Scenario helpers are smaller.
Per-file scenario wrappers are mostly gone.
Room identity is easier to scan.
Inventory and room placement are visible at the point of use.
```
