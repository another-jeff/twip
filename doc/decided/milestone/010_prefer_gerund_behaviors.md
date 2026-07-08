# Milestone 010: Prefer Viewing Behaviors to Noun-Specific Variants

Status:
All tests green.

Direction:
We are using behavior names that describe the reusable mechanic, not every possible object noun.

Prefer viewing-family behavior names for reusable viewing roles:

```text
ViewingCovered
ViewingObscured
ViewingConditioned
```

Do not implement every concrete noun as its own behavior:

```text
Blindered
Shuttered
Curtained
BlackoutCurtained
Fogged
Painted
Grimed
```

These are world/object details, not behavior classes.

Important design rule:
The noun belongs to the entity.
The mechanic belongs to the behavior.

"blinds", "curtains", and "shutters" are entity names/data.
`ViewingCovered` is the reusable behavior.

## Current implemented behavior

`ViewingCovered` lives in the external `twipx-viewing` package.

Distribution package:

```text
twipx-viewing
```

Import package:

```python
from twipx.viewing import ViewingCovered
```

Extension load path:

```python
load_extension("twipx.viewing")
```

`ViewingCovered` represents something that covers or partly covers a view through another thing.

```text
Handles:
  blinds
  vertical blinds
  curtains
  blackout curtains
  shutters
  boards
  paper over glass
  a painting over a peephole
  any other external/attached view cover

Key state:
  covers: str | None
    Optional entity id of the thing being covered.
    If None, the behavior can live directly on the looked-through entity.

  covering: bool
    Whether the covering is currently in front of the view.

  open: bool
    Whether the covering permits some view while still covering.

  open_uncovers: bool
    Whether "open" removes the covering from the view instead of merely opening a partial view.
```

Examples:

```text
lowered closed blinds:
  covering=True
  open=False

lowered open blinds:
  covering=True
  open=True

raised blinds:
  covering=False

closed curtains:
  covering=True
  open=False
  open_uncovers=True

open curtains:
  covering=False
  open=True
  open_uncovers=True

closed shutters:
  covering=True
  open=False
  open_uncovers=True

open shutters:
  covering=False
  open=True
  open_uncovers=True
```

## `LookThroughable` interaction

`LookThroughable` lives in the external `twipx-viewing` package.

It owns the `look through X` action.

It checks related `ViewingCovered` state before deciding what view message to return.

Current precedence:

```text
1. Closed/blocking ViewingCovered blocks the view.
2. Broken window may change the view message.
3. Open/partial ViewingCovered may change the view message.
4. Otherwise normal through-view message.
```

`LookThroughable` does not hard-import a concrete breaking extension.

It may inspect another behavior by stable behavior kind:

```python
behavior = entity.behaviors.get("breakable")

if getattr(behavior, "broken", False):
    ...
```

This keeps extension interaction possible without forcing hard dependencies between extension packages.

## Why this matters

We avoid a behavior explosion.

We still support rich world modeling.

We can add new scenery nouns by authoring entities differently, not by writing new behavior classes.

Core Twip no longer owns viewing behavior classes.

Core owns:

```text
parser
actions
verb policy
dispatch
world/entity state
behavior iteration
extension loading
```

`twipx-viewing` owns:

```text
LookThroughable
ViewingCovered
viewing-specific behavior semantics
```

## Deferred sibling behavior: `ViewingObscured`

`ViewingObscured` would represent the looked-through thing itself being hard or impossible to see through.

Likely examples:

```text
grime
paint
frost
fogged glass
soot
condensation
cracked/distorted glass
```

Likely shape:

```python
ViewingObscured(
    blocks=True,
    message="The glass is too fogged to see through.",
)

ViewingObscured(
    blocks=False,
    message="Through the fogged glass, the garden is only a blur.",
)
```

Difference from `ViewingCovered`:

```text
ViewingCovered is another thing in the way.
ViewingObscured is a condition of the looked-through thing itself.
```

Do not implement this until there is an actual gameplay case.

## Deferred sibling behavior: `ViewingConditioned`

`ViewingConditioned` would represent external/world conditions affecting the through-view.

Likely examples:

```text
darkness
weather
smoke outside
magical fog
time of day
room lighting
outside lighting
```

`ViewingConditioned` probably should not be implemented until the engine has clearer room/world/environment state.

Possible future examples:

```text
At night:
  "It is too dark outside to make out anything."

During heavy rain:
  "Rain streaks the glass, blurring the garden beyond."

During daylight:
  normal view message
```

Difference from `ViewingCovered` and `ViewingObscured`:

```text
ViewingCovered is another thing in the way.
ViewingObscured is a condition of the looked-through thing itself.
ViewingConditioned is a world/environment condition affecting the view.
```

Do not implement this until world/environment state exists.

## Deferred command semantics

`ViewingCovered` currently handles `open` and `close`.

Later it may need configurable command semantics for verbs such as:

```text
raise
lower
draw
pull
part
```

Do not add these until an actual gameplay case requires them.

Possible future shape:

```text
raise blinds:
  covering=False

lower blinds:
  covering=True

open blinds:
  open=True

close blinds:
  open=False

open curtains:
  covering=False

close curtains:
  covering=True

draw curtains:
  covering=True
```

These should be added as command semantics on the existing mechanic, not as noun-specific behavior classes.

## Guiding principle

Add a new behavior only when there is a new mechanic.

Do not add a new behavior merely because there is a new noun.
