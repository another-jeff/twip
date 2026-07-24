Library
/
twip-engine-roadmap.md


TWIP Engine Roadmap
Direction
TWIP should remain a small, deterministic, parser-first world engine rather than expanding prematurely into a full adventure-game framework.

The roadmap should favor features that prove or strengthen an abstraction. Adding a command is valuable when it clarifies the parser, action model, behavior system, world model, or extension surface—not merely because it increases the verb count.

Current Foundation
TWIP already has a functional vertical slice:

Text is parsed into a structured Action.

Verbs dispatch to command implementations.

Nouns resolve against visible or reachable scope.

The world supports rooms, inventory, containment, connectors, opening, locking, taking, dropping, and putting.

The prototype exercises a miniature playable loop.

Behaviors and twipx-* packages provide the beginnings of a composition and extension model.

Execution is deterministic and covered by automated tests.

Roadmap
1. Complete the Action Grammar
Fully support actions containing:

A verb

A direct object

A preposition

An indirect object

Representative commands:

put coin in box
unlock door with key
give book to librarian
ask librarian about ruins
This work includes consistent resolution, scope rules, ambiguity handling, missing-object errors, invalid-preposition errors, and verb registrations that describe accepted grammatical forms.

Outcome: New two-object verbs do not need their own miniature parser and resolver.

2. Establish an Action Lifecycle
Introduce a modest, explicit lifecycle:

parse
resolve
validate
perform
report
This should support shared preconditions, behavior participation, state mutation, failure handling, and success reporting without becoming a large event framework.

Outcome: Command implementations mostly contain only the logic unique to that action.

3. Stabilize Messages and Language Boundaries
Separate semantic action results from English phrasing.

Initial work may include:

Central message keys or message-producing functions

Consistent grammatical inputs

Fewer hard-coded sentence patterns in commands

Transcript tests for the default English renderer

Full internationalization is not required immediately. The first goal is a clean boundary.

Outcome: Standard wording can change without modifying parser, world, and command logic.

4. Expand Physical Interaction
Add a coherent set of interactions after the grammar and lifecycle are stable.

Possible verbs include:

close

lock and unlock

push and pull

wear and remove

give and show

insert and remove

switch on and switch off

The goal is to demonstrate clean behavior composition rather than maximize the number of verbs.

Outcome: Multiple actions reuse the same lifecycle and behavior infrastructure without awkward special cases.

5. Add Turns and Consequences
Introduce time as a deterministic engine concept:

Whether an action consumes a turn

A monotonically increasing turn counter

Scheduled events

State changes after a fixed number of turns

Optional per-turn behavior hooks

Examples:

The door closes after three turns.
The lamp burns out after twenty turns.
A guard moves between rooms.
Outcome: The world can change independently of the player’s immediate command while remaining reproducible.

6. Add Actors and Conversation
Generalize the player into one actor within the world.

Possible capabilities include:

NPC location and inventory

Giving and showing objects

Conversation topics

Actor movement

Commands directed to another actor

Actor-specific state or knowledge

Initial NPC behavior can use small state machines or behavior-driven responders rather than sophisticated AI.

Outcome: An NPC can move, hold objects, respond to a topic, and participate in ordinary actions.

7. Add Persistence and Authoring Support
Once the world model is stable enough:

Serialize mutable world state

Save and restore games

Validate entity references

Detect impossible containment or connector structures

Improve Python world-building helpers

Consider data-defined worlds where they provide clear value

The Python API should remain authoritative until the model is sufficiently settled.

Outcome: A prototype can save, exit, reload, and continue identically.

8. Stabilize the Extension Contract and Tooling
Define the supported public extension surface:

Public interfaces versus internals

Verb and behavior registration

Message registration

Compatibility expectations

Debugging and inspection commands

Transcript tooling

Additional twipx-* packages that prove the architecture

Outcome: An extension can add behaviors and verbs without importing private engine implementation details.

Proposed Order
Two-object grammar
    ↓
Action lifecycle
    ↓
Message boundary
    ↓
Broader interactions
    ↓
Turns and events
    ↓
Actors
    ↓
Persistence
    ↓
Stable extension API
Immediate Decision
The next task should be a small acceptance scenario that proves one or more foundational abstractions.

A strong candidate is:

unlock door with key
This scenario exercises:

Prepositions

Two-object resolution

Reachability

Behavior composition

State validation

Failure messages

The specific next implementation step should be chosen after checking the current repository so the roadmap follows the actual code rather than remembered state.