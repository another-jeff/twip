# Test Strategy

Twip tests are organized around contracts.

A test file name identifies the contract being tested.

Behavior and world contract tests live at the top level of `test/`:

```text
test/test_[contract].py
```

Preset wiring tests live under `test/preset/`:

```text
test/preset/test_[preset].py
```

Common contract forms:

```text
test/[behavior].py
test/[behavior]_[collaborator].py
test/world_[concern].py
test/preset/test_[preset].py
```

Examples:

```text
test/test_openable.py
test/test_lockable.py
test/test_openable_lockable.py
test/test_world_target_lookup.py

test/preset/test_door_wooden.py
test/preset/test_door_wooden_locked.py
```

Behavior tests prove behavior contracts, not presets.

A test in `test/test_openable.py` should pass for any entity with `Openable`.

A test in `test/test_lockable.py` should pass for any entity with `Lockable`.

The preset used in a behavior test is incidental. Prefer a small generic test entity over a real preset when testing behavior contracts.

Presets are tested separately. A preset test only proves that a packaged entity is wired correctly.

Preset tests may be grouped under `test/preset/` because they are numerous, intentionally terse, and focused on wiring rather than behavior contracts.

Example:

```text
test/test_openable.py
  proves Openable behavior

test/preset/test_door_wooden.py
  proves door_wooden includes Openable and expected aliases
```

For composed behavior tests, put the attempted behavior first and the collaborating behavior second.

Example:

```text
test/test_openable_lockable.py
```

This means:

```text
Openable is handling the attempted action.
Lockable affects whether that action succeeds.
```

Individual test names should be plain and consistent:

```text
test_open_closed_entity
test_open_already_open_entity
test_close_open_entity
test_close_already_closed_entity
test_lock_unlocked_entity
test_unlock_locked_entity
test_open_locked_entity_fails
test_open_unlocked_entity_succeeds
```

Prefer testing outcomes and state over exact message text.

Exact message assertions are allowed when wording is itself part of the decision. Otherwise, assert success/failure, state change, and a small meaningful message fragment when useful.

Every bug gets a regression test before the fix.
