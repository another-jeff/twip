# Milestone 009: parser prepositions / indirect targets

Current state:
- Dispatcher extraction is complete and green.
- `World.handle()` only parses text into `Action` and calls `dispatch(self, action)`.
- `World` owns state and scope helpers.
- `dispatcher.py` owns command/action routing policy.

Routing:
- `go <direction>` routes to movement.
- `move <direction>` routes to movement.
- `move <non-direction-target>` falls through to generic targeted component dispatch.
- Direction detection now uses `twip.direction`.

Direction module:
- Replaced `dir.py` with `direction.py`.
- Owns canonical direction constants:
  - `N`, `S`, `E`, `W`
  - `NE`, `SE`, `NW`, `SW`
  - `U`, `D`
  - `IN`, `OUT`
- Owns direction aliases.
- Owns `normalize(value: str) -> str`.
- Owns `is_direction(value: str) -> bool`.
- Parser and dispatcher both use this shared direction source.

Action:
- Action fields are standardized as strings.
- Missing action data is represented by `""`, not `None`.
- Current shape includes:
  - `verb`
  - `target`
  - `text`
  - `preposition`
  - `target_indirect`

Parser:
- Normalizes whitespace and lowercase.
- Empty input returns empty-string fields.
- Bare direction aliases become `go <direction>`.
- Verb aliases include:
  - `l -> look`
  - `x -> examine`
  - `i -> inventory`
  - `z -> wait`
  - `g -> again`
- Parser now handles prepositions and indirect targets.

Supported indirect-command parsing includes:
- `put coin in slot`
- `put book on table`
- `unlock door with key`
- `give coin to guard`
- `show badge to guard`
- `ask guard about boat`
- `tell guard about boat`

Preposition support includes:
- `at`
- `in`
- `into`
- `on`
- `onto`
- `under`
- `behind`
- `with`
- `to`
- `from`
- `about`

Prefix/postfix preposition handling exists:
- Prefix examples:
  - `look under rug`
  - `turn on lamp`
- Postfix examples:
  - `turn lamp on`
  - `take coat off`

Uniform Zebra progress:
- `WAIT` / `Z` implemented and green.
- `I` already covered by parser aliases.
- Direction aliases expanded and green.
- `PUSH it` implemented via `Pushable`.
- `PULL it` implemented via `Pullable`.
- `TURN it` implemented via `Turnable`.
- `TOUCH it` implemented via `Touchable`.
- `SMELL it` implemented via `Smellable`.
- `LISTEN` / `LISTEN it` implemented via `Listenable`.
- `READ it` implemented via `Readable`.
- `SEARCH it` implemented via `Searchable`.
- `TASTE it` implemented via `Tasteable`.
- `EAT it` implemented via `Eatable`.
- `DRINK it` implemented via `Drinkable`.
- Simple message components now share `MessageAction`.

Important design decisions:
- Prefer behavior names that describe command capability:
  - `Eatable`, not `Edible`
  - `Listenable`, not `Audible`
- Do not add verbs blindly from IF command sheets.
- Uniform Zebra is a coverage guide, not a command-bloat mandate.
- `rub` is probably an alias/variant of `touch`, not its own component yet.
- `kick`, `climb`, etc. are not simple message actions by default because they imply richer semantics.
- Indirect targets/prepositions are now parser structure, not behavior yet.

Current green count:
- Last seen: 203 tests passing.

Likely next step:
- Move past simple message verbs.
- Start implementing behavior that uses `preposition` and `target_indirect`.
- Good next candidates:
  - `put coin in slot`
  - `unlock door with key`
  - `look under rug`
  - `ask guard about boat`