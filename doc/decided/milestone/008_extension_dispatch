# Milestone 008: Extension Dispatch

Twip now has a working verb-first extension dispatch seam.

## Summary

World command handling is moving away from hard-coded verb behavior and toward component-owned behavior.

The parser recognizes interactive-fiction command shapes, but parser grammar is not semantics. Semantic overlap belongs in components and extensions, not in parser aliases.

## Parser policy

Parser aliases only safe shorthand forms:

* `l` -> `look`
* `x` -> `examine`
* `i` -> `inventory`
* `z` -> `wait`
* `g` -> `again`
* directions -> `go <direction>`

Important semantic boundary:

* `look`, `examine`, and `search` are distinct verbs.
* `x` aliases `examine`, not `look`.
* Components may choose to handle multiple verbs when that is semantically appropriate.

## Action shape

`Action` now supports:

* `verb`
* `target`
* `text`
* `preposition`
* `target_indirect`

This supports ordinary target commands, prepositional commands, and indirect-target command shapes such as:

* `search box`
* `dig in dirt`
* `unlock door with key`

## Verb policy

Seed verb policy lives in:

```text
src/twip/verb.py
```

`VERBS` records known verbs and target requirements.

World uses verb policy so targetless verbs that do not require a target can fall through to:

```text
Nothing happens.
```

Unknown verbs still require a target by default.

## Component dispatch contract

Component handlers now use this contract:

* `None` means the component did not claim the action; keep dispatching.
* `Result.success(...)` means the component claimed the action successfully; stop dispatching.
* `Result.failure(...)` means the component claimed the action unsuccessfully; stop dispatching.

Tests guard both sides:

* ignored actions continue to later components
* claimed failures stop dispatch

## Extension seam coverage

The generic extension seam now supports:

* ordinary target actions

```text
search box
```

* prepositional target actions

```text
dig in dirt
```

* indirect target inspection

```text
unlock door with key
```

* current-room targetless actions

```text
listen
```

* player targetless actions

```text
jump
```

* inventory item extension dispatch

```text
eat apple
```

* ambiguity across room and inventory scope

```text
eat apple
```

with two accessible apples produces an ambiguity failure.

## Dispatch order

Hard-coded legacy routes still exist for core behavior:

* inventory
* room look
* targeted look
* take
* drop
* go / move

Other targeted actions use generic entity/component dispatch.

Targetless extension dispatch runs in this order:

1. current room
2. player
3. verb-policy fallback

## Scope model

Twip now distinguishes visible scope from accessible scope.

Visible scope includes:

* current room
* room contents
* visible connectors

Accessible scope includes:

* visible scope
* player inventory

Current behavior:

* `take` still uses room-visible behavior and does not take inventory items.
* generic extension dispatch uses accessible scope.

## Examine / look / search boundary

`Lookable` now claims both:

* `look <target>`
* `examine <target>`

It does not claim:

* `search <target>`

This preserves the intended semantic boundary:

* parser aliases `x` to `examine`
* `Lookable` decides that examining a lookable thing returns its description
* `search` remains available for different future behavior

Representative tests:

```text
examine lamp -> Lookable description
x lamp       -> Lookable description
search lamp  -> not Lookable description
```

## Design decisions

* Parser grammar is not semantics.
* Parser aliases should stay conservative.
* Semantic aliasing belongs in components/extensions.
* `Lookable` may handle both `look` and `examine`.
* `search` remains distinct.
* `World` should resolve scope and dispatch actions.
* Components should own verb behavior wherever possible.

## Status

All extension-dispatch milestone behavior is green.

## Next direction

Continue moving behavior out of hard-coded `World` routes and into explicit component or extension claims.
