# Connector Sidedness

A connector is a shared entity that relates rooms or spaces.

Doors, gates, windows, archways, roads, and passages may be connectors.

A connector may have different parser-facing language and operation rules from each side.

## Shared state

Physical state belongs to the shared connector entity.

Example:

```text
door
  Openable = open | closed
  Lockable = locked | unlocked
```

There is one door.

There is one open state.

There is one lock state.

This is true even when the door is visible from multiple rooms.

## Side-local language

Each side of a connector may have local traits.

Example:

```text
same door

hall side:
  north door

kitchen side:
  south door
```

The direction words are local to the side.

They should not be global door traits.

## Side-local access

Some operations may be possible from one side but not another.

Example:

```text
deadbolt door

inside:
  can lock/unlock with thumbturn
  no key required

outside:
  can lock/unlock only with key
```

The lock state is shared.

The access rule is side-local.

```text
Lock state is global.
Lock access is side-local.
```

This avoids modeling one physical lock as two independent locks.

## Good model

```text
door
  Openable
  Lockable
  Connector

connector side: hall
  traits={"north"}
  lock access=thumbturn

connector side: porch
  traits={"south"}
  lock access=keyed
```

From the hall:

```text
unlock north door
  may succeed without key
```

From the porch:

```text
unlock south door
  may require key
```

Both commands operate on the same shared lock state.

## Deferred work

Key possession, inventory, permission checks, and actor equipment are later concerns.

For now, Twip only needs the design seam:

```text
connector side can carry local operation rules
```

Inventory is not magic.

Eventually:

```text
inventory = player.Container
```

But connector sidedness should not require inventory to exist yet.

## Rule

A connector has shared physical state.

A connector side has local language and local access rules.
