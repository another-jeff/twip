# Milestone: Inventory

Twip now supports a non-magic player inventory.

Inventory is ordinary world state:

```text
World.player_id -> player Entity
player Entity -> Container
Container.items -> carried entity ids
carried item -> Containable.parent = player.id
```

Implemented behavior:

```text
take <target>
  moves a visible Containable entity from its current Container
  into the player's Container

drop <target>
  moves a carried entity from the player's Container
  into the current room's Container

inventory
  lists entities in the player's Container
```

The player is not special because of its name.

```text
Entity named "player" is not enough.
World.player_id explicitly identifies the player.
```

Inventory is not a separate subsystem. It is containment.

```text
room contains item
player contains item
```

Scope rules:

```text
take searches visible current-room/world scope
drop searches only player inventory
inventory reads only player inventory
```

Ambiguity rules:

```text
ambiguous take fails without mutation
ambiguous drop fails without mutation
disambiguated take/drop use ordinary name + trait matching
```

Important regressions covered:

```text
take ignores same-named items in other rooms
take ignores same-named items already in inventory
drop ignores same-named visible room items
drop destination is World.current at drop time
inventory does not list visible room items
```

Design result:

```text
Inventory is player.Container.
```
