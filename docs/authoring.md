# Authoring a course

The runtime reads `content/catalog.yaml` and all `content/*/exercises/*.yaml`. The catalog has version 1
and a list of module maps with `language`, `id`, `title`, `docs`, and optional `roadmap: true`.

## Exercise schema

Required fields:

| Field | Meaning |
|---|---|
| `id` | Unique stable lowercase/hyphen ID |
| `language` | scala, c, rust or python |
| `module` | Registered module ID |
| `title`, `order` | Display title and positive sorting order |
| `prerequisites` | List of exercise IDs; all must be complete |
| `concepts` | Concept tags for detailed progress |
| `assignment` | Markdown with a concrete contract and workflow |
| `docs` | Contained path relative to content/ |
| `hints` | Ordered static hints, from broad to specific |
| `files` | Relative filename → text; support files only |
| `checks` | Nonempty ordered check list |
| `solution` | Relative filename → reference text; not copied to learner workspaces |

Optional fields: `project` (a stable project-directory slug) and `difficulty` (1..5).
Unknown exercise fields are errors. Prerequisite names and cycles are checked before the app starts.
Paths must remain inside their configured root. Do not use `.syntaxlab*` internal metadata names.

## Check schema

```yaml
checks:
  - type: file
    path: Main.scala
    label: Your source file exists
  - type: command
    args: ['$scala', test, '.', '--server=false']
    timeout: 240
    label: Scala compilation and tests
  - type: command
    args: ['$scala', run, '.', '--server=false']
    timeout: 240
    label: Application runs
```

`$scala`, `$cc`, `$cargo`, `$rustc`, and `$python` are replaced by configured executable names. Other arguments are literal: globbing,
pipes, shell expansion, and redirection do not happen. Optional `stdin` supplies input; optional `stdout`
compares output after stripping leading/trailing whitespace. Nonzero exit status always fails.
The runner also supplies CC to portable C test drivers.
An optional `requires: ['$cc']` list identifies tools invoked by a driver, so missing compilers are
reported as infrastructure errors before executing the driver.
Rust's Cargo checks declare `requires: ['$cargo', '$rustc']`; the runner supplies the configured compiler
through RUSTC. Use `$python` for Python course commands so local interpreter configuration is respected.

Construct-specific lessons may add `type: construct`, `path`, `pattern` (a Python regular expression),
and `label`. These are heuristics, not an AST parser. Favor behavior tests, and avoid exact source-text
comparisons that reject harmless formatting or alternative correct approaches.

## Scala support files

Every Scala lesson includes project.scala with pinned Scala 3 and test-only MUnit directives, plus one or
more `.test.scala` suites. A learner must be able to run `scala-cli test .` independently of SyntaxLab.
Test behavior, boundaries, negatives, empty collections, and repeated calls. Do not put the implementation
under test in the test file. A source-less fresh workspace is expected to fail compilation until the learner
creates the required definitions.

## C support files

Supply a portable Python driver invoking GCC with argument arrays, strict warnings and timeouts. The shipped
drivers compile the application, run it, then compile each implementation file with main renamed for linkage
to a separate assertion harness. Harness names start `test_` and are excluded from the application build.
Files shared by the implementation and harness belong in learner-created guarded headers.

The driver must test real behavior, including boundary/failure paths appropriate to the lesson. Keep test
artifacts in `.syntaxlab-build`. Never have tests write to a learner's personal paths. Use temporary files
for persistent-program CLI tests.

## Rust support files

Supply Cargo.toml with a stable package name, edition 2021, and the minimum supported compiler version.
The initial path requires Rust 1.70+ and uses no external crates. The learner creates src/main.rs and, for
library exercises, src/lib.rs. Tests in tests/*.rs import the public crate API or launch the Cargo binary
using CARGO_BIN_EXE_<package-name>. `cargo test` must work independently of SyntaxLab; checks use --offline
because the shipped courses need no crate downloads. Keep tests and reference implementations separate.

## Python support files

Supply tests/test_*.py with ordinary unittest.TestCase suites. They run from the root using
`python3 -m unittest discover -s tests -v`, with no framework dependency. Early output lessons use subprocesses
and supply deterministic stdin. Function lessons import main, so check that importing it performs no I/O.
The learner creates main.py and any requested modules. File tests use temporary directories and explicit UTF-8.

## Growing stages

Use the same `project` slug and language for all stages. Depend on the preceding stage and the skill lessons
needed for every new concept. Add uniquely named test/assignment files; do not change the contents of an
existing support filename. Keep earlier behavior stable and supply a complete reference snapshot per stage.
The C checker should list prior stage drivers as regression checks; Scala, Cargo and unittest discover
previously installed suites. Stage dependencies must include the skill concepts being applied. A standalone
reference snapshot plus the earlier support files should pass all cumulative tests.

## Documentation and learning quality

Explain the concept, give its syntax and an unrelated small example, list common mistakes, include useful
commands, and link related Markdown references. The assignment must state testable interfaces and input
domains without giving away the algorithm. Write two or more hints that reveal reasoning gradually.
Use older concepts in new work. Reduce syntactic reminders as the course progresses.

## Verification

```sh
syntaxlab validate
pytest -q
python tools/verify_content.py --exercise your-exercise-id
```

Edit the YAML and Markdown files directly; they are the canonical course sources. There is no required
code-generation step and no Python lesson registry to update. Keep stable IDs when revising a lesson so
existing progress remains associated with it. Existing learner support files are intentionally preserved;
use a new exercise ID for an incompatible contract, or have the learner explicitly back up/reset the workspace.
