# Containment and Connection

Twip distinguishes containment from connection.

Containment means one entity is located inside another entity.

Connection means one entity forms a boundary, route, or relationship between rooms.

These are different concepts and should not be collapsed.

## Containment

A contained thing has a containing place.

Examples:

```text
coin in room
book in box
apple in basket
item in player inventory
```

Containment is appropriate for entities that occupy a location and may later be moved, taken, dropped, hidden, revealed, or transferred.

```text
Room
  Container

Coin
  Containable
```

A room may contain things.

A coin may be contained by a room.

## Connection

A connected thing relates two or more rooms without being duplicated inside each room.

Examples:

```text
door between hall and kitchen
gate between yard and road
archway between chamber and corridor
window between room and outside
```

A door is not a coin-like object inside a room.

A door is a shared boundary between rooms.

```text
Door
  Openable
  maybe Lockable
  Connector
```

A door should not be copied into each room.

There should be one door entity with one shared state.

## Why this matters

Duplicating a door creates synchronization problems.

This is wrong:

```text
hall_north_door
  open

kitchen_south_door
  closed
```

Those would appear to be two different doors, even though the world fiction says they are one door.

The correct model is:

```text
one shared door
  visible from hall as north door
  visible from kitchen as south door
  one shared open/closed state
  one shared locked/unlocked state
```

## Rule

Containment models where things are.

Connection models how rooms relate.

A room contains things.

A door connects rooms.
