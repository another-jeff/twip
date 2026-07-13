# Milestone 011: Playable Prototype and CLI

Status: All tests green.

Twip now has a small playable world that exercises the engine through the same text-command interface intended for real games.

## CLI loop

Added:

```
src/twip/play.py
```

The CLI loop is deliberately thin.

It:

* accepts injectable `read` and `write` functions
* reads one command at a time
* sends nonblank commands to `World.handle()`
* writes the returned result message
* ignores blank input
* exits on `quit` or `exit`
* exits cleanly on EOF
* exits cleanly on Ctrl-C

The CLI does not own game rules or world state.

Its responsibility is only:

```
read command
pass command to world
display result
```

This keeps command execution testable without requiring a real terminal.

## Prototype world

Added:

```
example/prototype.py
```

The prototype contains:

* a front porch
* an entry hall
* north/south movement between them
* room names and descriptions
* a player with inventory
* a fixed desk
* an openable container box
* a takeable coin initially inside the box

The prototype exposes an injectable `run()` function so the complete game loop can be exercised in tests.

## Acceptance path

The prototype has an end-to-end acceptance test covering:

```
north
open box
look in box
take coin
inventory
put coin in box
look in box
inventory
quit
```

The test verifies:

* exact displayed output
* command sequencing
* room movement
* opening a container
* looking inside a container
* taking an object from a container
* inventory presentation
* putting an object back into a container
* final containment state
* clean CLI termination

## Testing boundary

The prototype acceptance test is intentionally broader than ordinary unit tests.

Unit tests continue to verify individual parser, command, behavior, scope, and world-state rules.

The prototype test verifies that those pieces work together through the public player-facing interface.

## Design decisions

### The CLI remains replaceable

Twip is not coupled to a specific terminal implementation.

A different interface may later provide commands through:

* another command-line front end
* a graphical interface
* a web application
* a test harness
* another process

All such interfaces should still ultimately send command text to the world and receive a `Result`.

### The example is executable documentation

The prototype is not a separate engine implementation.

It demonstrates how to:

* build a world
* add rooms and objects
* connect locations
* place the player
* run the command loop

The example should remain small enough to understand as a complete program.

### World state remains authoritative

The acceptance test checks final containment state rather than trusting output text alone.

Printed text describes what happened.

The world model determines what actually happened.

## Deferred

The prototype does not yet require:

* save or restore
* command history
* transcript files
* configurable prompts
* automatic room descriptions after every movement
* a full game launcher
* packaging example games as distributions
* terminal styling
* asynchronous input
* AI-assisted command interpretation

These should be added only when a concrete interface or gameplay requirement needs them.

## Guiding principle

A small playable world is more valuable than a large collection of disconnected engine features.

Every major engine capability should eventually be demonstrable through an executable example and an end-to-end acceptance path.
