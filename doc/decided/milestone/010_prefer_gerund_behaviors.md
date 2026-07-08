# Milestone 010: Prefer Gerund Behaviors to Noun-Specific Variants

Status:
All tests green.

Direction:
We are using behavior names that describe what is happening, not every possible object noun.

Prefer gerund-style behavior names for reusable mechanical roles:

```
ViewCovering
ViewObscuring
ViewConditioning
```

Do not implement every concrete noun as its own behavior:

```
Blindered
Shuttered
Curtained
BlackoutCurtained
Fogged
Painted
Grimed
```

These are world/object details, not behavior classes.

Current implemented behavior:

ViewCovering:
Represents something that covers or partly covers a view through another thing.

```
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

Examples:
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

Important design rule:
The noun belongs to the entity.
The mechanic belongs to the behavior.

"blinds", "curtains", and "shutters" are entity names/data.
ViewCovering is the reusable behavior.

LookThroughable interaction:
LookThroughable owns the "look through X" action.

It checks related ViewCovering state before deciding what view message to return.

Current precedence:
1. Closed/blocking ViewCovering blocks the view.
2. Broken window may change the view message.
3. Open/partial ViewCovering may change the view message.
4. Otherwise normal through-view message.

Why this matters:
We avoid a behavior explosion.
We still support rich world modeling.
We can add new scenery nouns by authoring entities differently, not by writing new behavior classes.

Deferred sibling behaviors:

ViewObscuring:
Represents the looked-through thing itself being hard or impossible to see through.

```
Likely examples:
  grime
  paint
  frost
  fogged glass
  soot
  condensation
  cracked/distorted glass

Likely shape:
  ViewObscuring(
      blocks=True,
      message="The glass is too fogged to see through.",
  )

  ViewObscuring(
      blocks=False,
      message="Through the fogged glass, the garden is only a blur.",
  )

Difference from ViewCovering:
  ViewCovering is another thing in the way.
  ViewObscuring is a condition of the viewed-through thing itself.
```

ViewConditioning:
Represents external/world conditions affecting the through-view.

```
Likely examples:
  darkness
  weather
  smoke outside
  magical fog
  time of day
  room lighting
  outside lighting

Likely shape:
  ViewConditioning probably should not be implemented until the engine has clearer room/world/environment state.

Possible future examples:
  At night:
    "It is too dark outside to make out anything."

  During heavy rain:
    "Rain streaks the glass, blurring the garden beyond."

  During daylight:
    normal view message
```

Deferred command behavior:
ViewCovering currently handles open/close.

Later it may need configurable command semantics for verbs such as:
raise
lower
draw
pull
part

Do not add these until an actual gameplay case requires them.

Possible future shape:
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

Guiding principle:
Add a new behavior only when there is a new mechanic.

Do not add a new behavior merely because there is a new noun.
