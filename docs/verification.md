# Implementation verification

## Rust and Python extension — 2026-10-09

- Catalog: **180 exercises/stages and 62 module documents** across Scala, C, Rust and Python. Both new
  languages include 30 skill exercises and a 10-stage growing project, with Markdown references and roadmaps.
- Application suite: **85 passed, 3 skipped**. The skips are the real Cargo tests; Rust/Cargo are not installed
  in this environment. Tests cover four-language navigation/selection, CLI commands, tool configuration,
  no-overwrite workspaces, growing-stage regression files, missing-tool diagnostics and new-path persistence.
- Ruff passed; Mypy passed for all 11 application modules. `syntaxlab validate`, `status` and `doctor`
  ran against the checkout: the new paths appear at 0%, existing Scala progress/current selection remain,
  and doctor identifies the missing Rust toolchain. GNU Make is now available on this machine.
- **All 40 Python reference snapshots passed** ordinary unittest checks, import-safety checks and program
  execution, including the final Study Planner's subprocess-based persistent CLI and invalid-data paths.
- Rust definitions, Cargo manifests, prerequisites and workspace support files validate. **All 40 Rust
  reference execution checks were explicitly skipped** due to missing `cargo` and `rustc`; Rust compilation
  and runtime behavior have not been verified here. These are not recorded as passing checks.
- The database upgrade test preserves existing Scala/C attempts, completion timestamps, current selection
  and hint usage while registering the new languages and content. No learner workspaces are used by tests.
- `cargo test` and `python3 -m unittest discover -s tests -v` are the standalone learner test interfaces;
  neither course requires external test libraries. Rust exercises use no crates.io dependencies.

Install Rust from [rustup.rs](https://rustup.rs/), reopen the shell, and verify the Rust path with:

```sh
rustc --version
cargo --version
syntaxlab doctor
python tools/verify_content.py --language rust
pytest -q
```

The original implementation's verification record follows; its tool availability and zero-progress state
describe that earlier run rather than the current learner database.

---

Verified locally on 2026-10-06 using Python 3.14.6, Textual 1.0.0, Scala CLI 1.16.0,
OpenJDK 25.0.4, Scala 3.3.7, MUnit 1.0.4, and GCC 13.3.0.

## Application

- **62 pytest tests passed**, using isolated temporary roots and databases.
- `ruff check syntaxlab tests tools`: passed.
- `mypy syntaxlab`: passed, all 10 application modules.
- Course validation: **100 exercise/stage definitions, 33 module definitions**; no missing prerequisites
  or cycles. Every path is reachable through the dependency graph.
- Real console launch in a pseudo-terminal, rendered dashboard, and keyboard quit: passed.
- Textual pilot checks: language/project switching, module filtering, Enter workspace creation, locked
  content, documentation links, progress view, and background checking/persistence passed.
- CLI help, initialization, status, detailed progress, documentation, projects, continue, hints,
  explicit solution/reset confirmation, current-directory checking, and missing-editor handling passed.
- SQLite migrations, future-version rejection, catalog metadata, attempt history, completions, unlocks,
  and repeated read-only operations without binary/mtime churn passed.
- Reopening preserves learner source and edited support files. Reset backs up source. Project stages reuse
  their directory and retain earlier tests. Symlink escapes and malformed metadata are rejected.
- Git checkpoint tests cover refusal of unrelated/staged changes, scoped staging, and hook-failure propagation.
  No project commit was created during verification.

## Real language toolchains

- **All 50 Scala skill/stage reference snapshots passed** their MUnit/structural checks and application runs.
- Plain **`scala-cli test .`** passed independently for a generated first exercise and the final growing
  Scala project, including every earlier stage suite. The final project additionally tests its command loop
  and EOF behavior through Main, not just its helper methods.
- **All 50 C skill/stage snapshots passed GCC compilation and behavioral verification**, with strict warnings.
  This includes arrays, strings, pointer operations, allocation/reallocation, headers, file I/O, cumulative
  project regressions, and the final task manager's subprocess-based persistence/error-path tests.
- Reference tests were written only into disposable temporary workspaces. Learner progress remains 0%.

## External dependency limitation

**GNU Make is not installed in this environment.** `syntaxlab doctor` correctly reports it missing and
returns a nonzero status. Five Make invocations across the Make lesson and final C stages were explicitly
reported as skipped by the content verifier. Their C programs were compiled and executed with GCC,
including the final CLI, but this does not substitute for running the Make recipes.

To enable those remaining environment-dependent checks on Ubuntu/WSL:

```sh
sudo apt install build-essential
source .venv/bin/activate
syntaxlab doctor
python tools/verify_content.py --language c
```

No system packages were automatically installed. All other required tools, including the VS Code CLI,
were found. The main SQLite database is deliberately included in Git's index; no WAL/SHM/journal files
are included. Application/source changes are left uncommitted.
