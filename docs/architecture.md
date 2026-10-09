# Architecture

SyntaxLab is deliberately a small Python package with clear service boundaries. No server is involved.

| Module | Responsibility |
|---|---|
| `config.py` | Repository discovery, TOML defaults, contained paths, user-facing LabError |
| `languages.py` | Shared supported-language order for CLI, validation, persistence and TUI |
| `courses.py` | Typed Exercise records, YAML loading/validation, module catalog, dependency graph |
| `progress.py` | All SQL, numbered migrations, short-lived connections, attempts and completion state |
| `workspace.py` | Safe creation, no-overwrite support files, ancestor discovery, backup/reset |
| `runner.py` | Argument-array processes, environment/cwd, timeouts, diagnostics, explicit Git checkpoint |
| `checks.py` | Declarative checks, fail-fast execution, attempt recording, infrastructure distinction |
| `service.py` | Coordinates the above and enforces prerequisites before preparing work |
| `cli.py` | argparse command surface and Rich output |
| `tui.py` | Textual dashboard, filtering, references, hints, background checking/editor launch |

The interfaces are intentionally file-oriented. An Exercise contains assignment Markdown, support files
(never learner code), visible behavior tests, check specifications, and a private reference snapshot.
The catalog is immutable for a running session. Loading validates all prerequisites, including cycles.
Module roadmap entries can have no exercises; they are not counted in implemented progress percentages.

## State and migrations

`PRAGMA user_version` is the schema version. `MIGRATIONS` is an ordered list of transactional SQL scripts;
adding a migration is append-only. Opening a future schema produces an actionable error.
Schema version 1 stores languages, modules, exercises, project stages, timestamped attempts, timestamped
completions, current selection and hint counters, and documentation/solution encounters.
Completed project stages are project_stages joined with completions by exercise ID.

Catalog synchronization only writes changed/new metadata. All queries open and close a connection.
Default DELETE journaling avoids long-lived WAL state; transactions prevent partially recorded checks.
An attempt contains per-check results, diagnostics and infrastructure flags. Completion is awarded only
when every check passes. Failed revisits retain prior completion. Reset explicitly invalidates descendants
while retaining attempt history. No automatic database compaction or VACUUM churns the binary Git file.

## Execution and safety boundary

Student programs are local programs with the user's permissions. There is no hostile-code sandbox.
Commands never pass through a shell; timeouts kill a Linux process group. File operations check contained
resolved paths. Workspace symlink aliases are rejected. Creation uses exclusive file writes, so repeated
opens preserve learner files; the internal exercise marker changes atomically when selecting project stages.
Reset moves a workspace to a uniquely named backup rather than deleting it.

Checks stop at the first failure. In particular, a failed compile cannot accidentally run an old executable.
GCC diagnostics and Scala/MUnit output are preserved. Missing executable/cwd errors are infrastructure
failures; failed assertions and compiler errors are learning feedback. Visible tests are normal files that
learners can extend; this is not an assessment security system. Construct checks are intentionally labeled
heuristics, used only where practicing that syntax is the lesson's objective.

## Projects

Each project maps every stage to one directory. New stages add new support/test filenames and update the
internal marker; they never migrate or rewrite learner source. Scala discovers all `.test.scala` files;
C stages carry a cumulative list of prior test commands. Stable earlier APIs are part of each project contract.
Reference snapshots let the maintainer verifier validate every stage independently, including cumulative tests.

## Extending

Add data for new lessons, not Python conditionals. Add a new check kind only when a real behavioral need
cannot be expressed with a normal program/harness. Put persistence changes in a migration and test upgrades
from an earlier version. The Textual app and CLI share Lab, Catalog, Progress, Workspaces and the same checker.
Thread workers keep compilation off the UI loop, and SQLite connections never cross thread boundaries.

## Rust and Python paths

All four languages share the same check engine and workspace lifecycle. Configured `$cargo`, `$rustc`, and
`$python` executable substitutions extend `$scala`/`$cc`; Cargo receives RUSTC through the runner environment.
Rust commands declare their tool requirements so missing Cargo/compiler installations are infrastructure
failures. Cargo.toml configures ordinary standard-library-only binary/library crates, with integration tests
under tests/. Python uses standard-library unittest discovery and import-safe entry points. The application
does not need pytest installed in learner workspaces.

Language IDs are ordinary SQLite text keys: adding Rust/Python requires catalog synchronization, not a schema
reset or destructive migration. Existing completions/attempts/current selection stay intact. CLI `continue`
uses the current exercise's language unless another one is explicitly requested. The TUI has a direct
language selector as well as the L cycle shortcut.
