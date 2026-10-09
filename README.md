# SyntaxLab

**Read → understand → write from scratch → compile → debug → test → progress.**

SyntaxLab is a local programming-learning environment for Linux and WSL. Its Textual dashboard
organizes your learning; **VS Code is your editor, and your real shell is your terminal**.
There is no browser, account, remote execution, telemetry, or AI service.

The course includes **180 exercises and growing-project stages** across four languages:

| Path | Skills | Project stages | Initial coverage |
|---|---:|---:|---|
| Scala 3 | 39 | 11 | Foundations, functions, control flow, collections, matching, recursion, classes/constructors, records, Option, enums, organization, testing |
| C | 35 | 15 | Foundations, control flow, functions, arrays, strings, pointers, structs, recursion, heap memory, headers, Make, file I/O |
| Rust | 30 | 10 | Cargo, foundations, functions, control flow, ownership/borrowing, slices, collections, structs/methods/traits, enums, Option/Result, recursion, modules, files, testing |
| Python | 30 | 10 | Foundations, functions, control flow, collections, exceptions, recursion, classes/dataclasses, modules, generators, UTF-8/JSON files, testing |

Scala's **Task Desk** becomes an interactive task manager. C's **Task Ledger** becomes a
multi-file, heap-backed CLI with persistent task files. Each project keeps one directory throughout
its stages. Rust's **Task Trail** and Python's **Study Planner** each become persistent CLIs over ten
stages, with ordinary Cargo or unittest regression tests. Advanced module roadmaps are visible in the documentation and progress views; they are
explicitly marked as planned, rather than counted as implemented exercises.

## Requirements

- Linux or Ubuntu under WSL; Python **3.11+** with venv/pip
- Git
- VS Code with the WSL extension and a working `code` command
- [Scala CLI](https://scala-cli.virtuslab.org/install/) and a JDK (17 or newer recommended)
- GCC and GNU Make (`build-essential` on Ubuntu)
- Rust **1.70+** and Cargo for the Rust course ([rustup installation](https://rustup.rs/))
- Python **3.11+** for the Python course; its tests use standard-library `unittest`, with no extra packages

The application and all learner programs execute locally. Scala CLI needs network access to fetch
compiler/test artifacts on first use, then uses its local cache. Workspaces pin **Scala 3.3.7** and
**MUnit 1.0.4**. No sbt is required. C uses C17 and `-Wall -Wextra -Wpedantic`; the visible verifier also
uses `-Werror` to make warnings actionable.
Rust projects use the 2021 edition and the standard library only. Once the toolchain is installed,
`cargo test --offline` works without downloading crates. Cargo.lock is deliberately **not** ignored;
commit it with your Rust binary projects. `target/` build output is ignored.

## Install and start

From this repository:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
syntaxlab doctor
syntaxlab
```

The console command is installed by pip. Keep the virtual environment active in each new shell.
This is a repository-first application: keep the course content alongside the source and use the
editable install above. Commands discover the repository from your current directory or fall back
to this editable checkout. `syntaxlab --root /path/to/SyntaxLab status` selects another checkout explicitly.

The database initializes automatically. `syntaxlab init` is also available; it is safe to repeat.
The included `data/progress.db` stores the catalog and your learning progress. Catalog updates add new
languages/lessons without resetting attempts, completions, hint use, or the current exercise.

### First lesson

Launch `syntaxlab`, choose a lesson with the arrow keys, press **D** to read the reference, then
**O** to open its workspace in VS Code. **L** cycles Scala → C → Rust → Python, or choose a language
directly in the sidebar selector. `continue` stays in the current language after completing a lesson;
use `--language` to switch explicitly.

For a CLI-only start:

```sh
syntaxlab continue --language scala
syntaxlab open
cd workspaces/scala/scala-hello
# Create Main.scala yourself, following ASSIGNMENT.md.
scala-cli run .
scala-cli test .
syntaxlab check
```

A freshly created workspace deliberately has **no learner source file**. Its tests will report missing
definitions until you write your program. Configuration, instructions, and ordinary test files are supplied;
function skeletons and solutions are not. Early lessons give explicit syntax; later contracts assume
you remember earlier material.

## Dashboard

| Key | Action |
|---|---|
| ↑ / ↓ | Select a lesson or stage |
| Enter | Create/reopen the selected workspace and show its path |
| O | Open the selected workspace using `code <path>` |
| C | Check in a background worker; show compiler/test diagnostics |
| D / B | Documentation / return to assignment |
| H | Reveal the next static hint |
| L | Cycle through all four languages (or use the language selector) |
| P | Switch between skills and growing projects |
| G | Module progress and advanced roadmap |
| Tab | Move focus between controls; the module selector filters the path |
| Q | Quit |

Completed, available, and locked lessons have distinct indicators. You can read locked assignments
and references, but workspace creation/checking follows prerequisites. Completed lessons remain revisitable.
Use a terminal around 100×35 or larger for the most comfortable split view.

## Commands

```text
syntaxlab                              Interactive dashboard
syntaxlab init                         Initialize/validate local state
syntaxlab doctor                       Versions, missing tools, database and course health
syntaxlab validate                     Validate every course definition and dependency graph
syntaxlab status                       Overall/language progress and current exercise
syntaxlab progress                     Modules and concepts in detail
syntaxlab continue [exercise-id]        Prepare the current/next available exercise
syntaxlab continue --language c         Continue a particular language
syntaxlab continue --language rust      Start/resume Rust
syntaxlab continue --language python    Start/resume Python
syntaxlab open [exercise-id]            Open in VS Code; use current workspace when inside one
syntaxlab check                        Check the exercise containing the current directory
syntaxlab docs                         Documentation index
syntaxlab docs scala functions         Show a Markdown reference in the terminal
syntaxlab docs c pointers
syntaxlab docs rust ownership
syntaxlab docs python functions
syntaxlab projects                     Stages, prerequisites and project progress
syntaxlab hint [exercise-id]            Next hint, without penalty
syntaxlab solution [exercise-id]        Explicit confirmation before revealing a reference
syntaxlab reset <exercise-id>           Confirm, back up work, then reset
syntaxlab reset <exercise-id> --yes     Explicit noninteractive reset confirmation
syntaxlab check --checkpoint            After a passing project check, request a Git checkpoint
```

IDs appear in `syntaxlab projects`, workspace directory names, and YAML files. For example,
`scala-functions-multiple`, `c-pointers-swap`, `scala-task-desk-01`, and `c-task-ledger-01`.
New-path examples: `rust-borrowing`, `python-dataclasses`, `rust-task-trail-01`, and `python-study-planner-01`.
`check` discovers `.syntaxlab.json` by walking up from your current directory, including nested source
directories. It does not guess an exercise from an unrelated working directory.

### C workflow

```sh
syntaxlab continue --language c
syntaxlab open
cd workspaces/c/c-hello
# Create main.c.
gcc -std=c17 -Wall -Wextra -Wpedantic main.c -o program
./program
python3 test_exercise.py
syntaxlab check
```

The supplied Python test driver has no SyntaxLab dependency: it compiles the real application,
runs it, then (for function exercises) compiles a visible C assertion harness against your functions.
It renames your main during the harness build and excludes `test_*.c` from the application link.
Compiler diagnostics are preserved. Do not compile all `.c` files indiscriminately: test harnesses
have their own main functions. Test executables/object files live in ignored `.syntaxlab-build/`.

### Rust workflow

```sh
syntaxlab continue --language rust
syntaxlab open
cd workspaces/rust/rust-hello
# Create src/main.rs yourself; Cargo.toml and integration tests are supplied.
cargo run
cargo test
syntaxlab check
```

Later skills ask you to create `src/lib.rs` with a public API and `src/main.rs` as a runnable demo.
Tests under `tests/*.rs` import the `syntaxlab_exercise` crate. The growing project uses the `task_trail`
crate instead. Ownership, borrowing, mutable references and slices have a dedicated progression before
more complex collections and models. No learner source is generated by `continue` or `open`.

### Python workflow

```sh
syntaxlab continue --language python
syntaxlab open
cd workspaces/python/python-hello
# Create main.py yourself.
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

The test suites are ordinary Python files under `tests/`. Early lessons execute the script and verify
stdout/stdin; later lessons import its functions and check behavior, errors, and state independence.
Use `if __name__ == "__main__":` to keep imports silent. Python's tests require no pip-installed framework.

### Growing projects

Complete the skill prerequisites, inspect `syntaxlab projects`, then select an unlocked stage:

```sh
syntaxlab continue scala-task-desk-01
syntaxlab open
# Work in projects/scala/task-desk; later stages reopen this same path.
```

Each new stage adds uniquely named tests and `STAGE-XX.md`; previous tests remain regression checks.
Advancing a stage does **not** rewrite your code, README, configuration, or existing test files.
Preserve earlier API contracts as the implementation grows. A project's Scala test run discovers
all installed stage suites; the C checker runs the cumulative stage drivers.

At the final stages:

```sh
# Scala project:
scala-cli run . -- --interactive
# Commands: add Read book, list, done 1, quit

# C project:
make
./program add tasks.txt 'Read a book'
./program list tasks.txt
./program done tasks.txt 1
```

Task Desk stores tasks for one session; Task Ledger explicitly saves tasks to the file you provide.
Task Trail and Study Planner also persist explicitly to the supplied path:

```sh
# projects/rust/task-trail, after the final stage:
cargo run -- add tasks.txt 'Read a book'
cargo run -- list tasks.txt
cargo run -- done tasks.txt 1

# projects/python/study-planner, after the final stage:
python3 main.py add tasks.json 'Read a book'
python3 main.py list tasks.json
python3 main.py done tasks.json 1
```

Rust discovers all installed stage integration tests with `cargo test`; Python discovers all stage suites
with `python3 -m unittest discover -s tests -v`. Both include real subprocess-based final CLI tests and
failure paths that protect corrupt input files from being silently overwritten.

## Your work is preserved

- Definitions under `content/` are separate from work under `workspaces/` and `projects/`.
- Reopening an existing exercise does not regenerate its files.
- Reference solutions stay in course-author data and appear only after the `solution` confirmation.
  This is a learning aid, not an anti-cheating system; the entire repository is yours to inspect.
- Reset moves the existing directory into **`backups/`**, then creates a fresh workspace. Nothing in
  the backed-up learner directory is deleted. Resetting a project stage resets the **whole project**.
- Reset also invalidates dependent completions to keep prerequisites consistent; historical attempts remain.
- Earlier-stage visits keep later installed project tests. Use Git history to inspect an earlier snapshot.

## Using SyntaxLab on multiple computers

Use **one computer at a time**, and keep this whole directory as one Git repository:

```sh
git pull
source .venv/bin/activate
syntaxlab
# Work, compile and check.
git add .
git commit -m "Practice Scala functions"
git push
```

On the other computer, clone/pull the same repository and create its own local virtual environment
using the installation instructions. Workspaces and projects are included in Git.
**`data/progress.db` is deliberately committed**, so attempts, completions, current exercise, hint use,
and project progress travel with your code. The application never automatically pulls, pushes, or commits.

SQLite uses short transactions and closes every connection. Read-only commands and repeated initialization
do not rewrite an unchanged database. The main DB is not ignored; `*.db-wal`, `*.db-shm`, `*.db-journal`,
compiler caches, binaries, and virtual environments are ignored. Quit active checks before syncing.

SQLite is a binary file: Git cannot meaningfully merge simultaneous progress edits. If both computers
changed it, retain a backup of both, choose the intended authoritative database, and recheck any missing
completions on that version. Avoid this by pulling before learning and pushing before switching computers.

### Optional stage checkpoints

From a project workspace, `syntaxlab check --checkpoint` is explicit permission to create a commit after
the stage passes. It stages only that project and the configured progress DB. It refuses when unrelated
changes or already-staged changes are present, so you can review and commit manually. Git identity must
already be configured. Hooks run normally; a rejected hook is reported and staged files remain available
for your review. There are no automatic commits during ordinary learning.

## Configuration

Defaults work without configuration. Optionally create `syntaxlab.toml` at the root:

```toml
editor = "code"
scala = "scala-cli"
cc = "gcc"
cargo = "cargo"
rustc = "rustc"
python = "python3"
timeout = 120
database = "data/progress.db"
```

Tool values are executable names or paths, **not shell command strings**. Commands always use argument
arrays. Course checks can specify a timeout; Scala checks allow 240 seconds for cold compilation/downloads.
The C driver limits each compilation/program invocation to 10 seconds. SyntaxLab kills the process group
on its outer timeout so child processes do not keep running. Database/workspace paths must remain in the
checkout; symlink escapes and workspace aliases are rejected. This is not a hostile-code sandbox.

## Developer setup and checks

```sh
pip install -e '.[dev]'
pytest -q
ruff check syntaxlab tests tools
mypy syntaxlab
syntaxlab validate

# Real toolchain checks of every private reference in disposable temporary workspaces:
python tools/verify_content.py --language c
python tools/verify_content.py --language scala
python tools/verify_content.py --language rust
python tools/verify_content.py --language python
python tools/verify_content.py --exercise scala-hello --plain-scala
```

Application tests use temporary roots/databases, cover CLI and Textual navigation, and run representative GCC,
Python and Cargo checks when their tools are installed. The content verifier separately executes reference implementations,
including cumulative growing-project tests. It returns 1 on a failed check or 2 when tool-dependent
checks were skipped. Reference verification never populates your real workspaces or progress DB.

See [architecture](docs/architecture.md) and [course authoring](docs/authoring.md).

## Adding exercises and documentation

Add an exercise YAML under `content/<language>/exercises/`; register a module in `content/catalog.yaml`
if necessary. Each lesson specifies its stable ID, prerequisites, concepts, assignment, support files,
checks, static hints, reference solution, and Markdown reference path. Run `syntaxlab validate` and
the reference verifier. The runtime has no hardcoded lesson switch statements.

Documentation lives in ordinary `content/<language>/docs/*.md` files. Include an explanation, syntax,
independent examples, mistakes, commands, and links to related local references. Solutions belong in
the exercise's author data, never in ordinary learner test files.

YAML and Markdown are the canonical course sources. Adding or editing a lesson requires no Python
application changes. `tools/verify_content.py` checks the reference snapshots in disposable workspaces.

## Troubleshooting

- **Missing tool:** `syntaxlab doctor` names the command and installation action. On Ubuntu,
  `sudo apt install build-essential` provides GCC and Make; `sudo apt install default-jdk` provides Java.
  These are commands for you to run; SyntaxLab never installs system software.
- **VS Code command missing:** install VS Code on Windows with its WSL extension, open a WSL shell, and
  verify `code --version`. Workspace creation still succeeds and its path is printed if editor launch fails.
- **Scala downloads/timeouts:** run `scala-cli test .` directly to finish the first download and inspect
  network/proxy errors, then retry. Pinned dependencies do not eliminate the initial download.
- **Scala main selection:** early exercises should have one entry point. Additional demos can be run with
  `scala-cli run . --main-class YourEntryName`.
- **Compiler/test failures:** preserve the diagnostic, fix the first compiler error, then rerun. A failed
  check is stored as an attempt; it does not complete the exercise or erase an earlier completion.
- **Make unavailable:** Python and Scala workflows and GCC-driven C lessons still run; Make lessons/stages
  require GNU Make.
- **Rust/Cargo unavailable:** install the stable toolchain from [rustup.rs](https://rustup.rs/), then reopen
  your shell (or source `$HOME/.cargo/env`) and run `rustc --version`, `cargo --version`, and `syntaxlab doctor`.
  SyntaxLab can still show Rust documentation and create workspaces before the toolchain is installed.
  Missing Rust tools are reported as infrastructure errors, not learner test failures.
- **Python imports seem to hang:** remove unguarded input() calls from module-level code and put the demo
  behind a main guard. Run the unittest command from the workspace root.
- **Course validation error:** the CLI reports the offending definition/context. Fix that YAML before
  opening the dashboard. Unknown prerequisites and cycles are rejected.
- **Database newer than application:** update this checkout instead of modifying user_version manually.
- **Database merge conflict or corruption:** preserve a backup, restore a known-good DB from Git, then
  recheck the affected workspaces. Your source files are stored separately.

## Repository layout

```text
syntaxlab/          Python app: CLI, Textual UI, services, course loader, SQLite, runner, workspaces
content/
  catalog.yaml     Module definitions and roadmap
  scala/           50 exercise/stage YAMLs and Markdown references
  c/               50 exercise/stage YAMLs and Markdown references
  rust/            40 exercise/stage YAMLs and Markdown references
  python/          40 exercise/stage YAMLs and Markdown references
workspaces/        Learner skill work (tracked)
projects/          Long-lived learner projects (tracked)
data/progress.db   Versioned SQLite progress (tracked)
docs/              Architecture and authoring guide
tests/             Application tests, including Textual pilot tests
tools/             Maintainer reference verifier
```
