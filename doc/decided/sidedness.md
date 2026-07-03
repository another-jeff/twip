# Portal Sidedness

A portal is a shared entity that connects rooms.

Doors, gates, windows, archways, and passages may be portals.

A portal may have different parser-facing language and operation rules from each side.

## Shared state

Physical state belongs to the shared portal entity.

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

Each side of a portal may have local traits.

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
  Portal

portal side: hall
  traits={"north"}
  lock access=thumbturn

portal side: porch
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
portal side can carry local operation rules
```

Inventory is not magic.

Eventually:

```text
inventory = player.Container
```

But portal sidedness should not require inventory to exist yet.

## Rule

A portal has shared physical state.

A portal side has local language and local access rules.
