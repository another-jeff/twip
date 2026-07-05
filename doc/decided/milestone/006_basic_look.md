# Milestone: Look

Twip now supports room look and targeted look.

Implemented behavior:

```text
look
  describes the current room
  includes current room Lookable text when present
  lists current room contents

look <target>
  describes a visible or carried Lookable entity
```

Room look is world-level:

```text
look
  uses World.current
  reads the current room entity
  reads current room Container
  does not require World.player_id
```

Room descriptions are component-based:

```text
room Entity -> Lookable
Lookable.text -> room description text
```

Room contents are containment-based:

```text
room Entity -> Container
Container.items -> visible current room contents
```

Room look scope rules:

```text
look lists only current room contents
look does not list inventory contents
look does not list items in other rooms
look lists multiple current room contents
look lists contents deterministically by name
```

Targeted look uses normal entity behavior:

```text
look coin
  resolves target
  dispatches to coin.Lookable
```

Targeted look scope is broader than take/drop:

```text
look <target> searches current room + player inventory
take <target> searches current room/world visible scope
drop <target> searches player inventory only
```

Targeted look rules:

```text
visible Lookable target succeeds
carried Lookable target succeeds
visible non-Lookable target fails cleanly
carried non-Lookable target fails cleanly
same-named room + inventory targets are ambiguous
same-named targets in other rooms are ignored
ordinary trait/name disambiguation works across room + inventory scope
```

Design result:

```text
Lookable is the description behavior.
Bare look describes current room.
Targeted look describes a selected visible or carried entity.
```
