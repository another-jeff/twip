# Documentation

This folder contains design notes, project decisions, and implementation guidance for Twip.

Twip documentation should favor small, stable facts over speculative architecture.

## Folders

```text
doc/
  README.md
  decided/
    style.md
    milestone_0.md
```

## Conventions

Use `doc/decided/` for decisions that are settled enough to guide implementation.

Use ordinary `doc/` files for notes that are still exploratory, unstable, or under discussion.

When a design choice becomes firm, move it into `doc/decided/`.

## Documentation goals

Documentation should help a person or agent make the next small correct change.

Prefer:

* concrete examples
* current project structure
* invariants
* naming rules
* regression expectations

Avoid:

* broad speculation
* future feature promises
* large abstract taxonomies before code exists
* describing behavior that is not represented by tests
