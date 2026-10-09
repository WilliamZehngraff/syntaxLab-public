# Growing project · Task Desk

## A program that grows with you
Task Desk begins as a greeting and becomes an interactive, testable task manager with immutable records,
a mutable class boundary, command parsing, optional lookup and multiple source files.
Every stage opens the **same** projects/scala/task-desk directory. Keep earlier behavior and tests.
Select a stage with `syntaxlab continue <stage-id>`; list IDs with `syntaxlab projects`.

## Design and syntax reference
Separate input/output from calculations. A parser turns text into a command; an operation updates state;
the entry point prints results. A tiny independent example:
```scala
def cleanInput(line: String): String = line.trim
val text = scala.io.StdIn.readLine()
if text != null then println(cleanInput(text))
```
End-of-file returns null from Java-style input APIs; contain that boundary rather than spreading null through
your model. Use Option for missing tasks. Keep earlier helper APIs to satisfy regression tests.

## Common mistakes
- Replacing the whole program at each stage loses valuable earlier work. Extend it instead.
- Do not put mutable task state in a global singleton when separate Board instances should be independent.
- Preserve IDs when editing task status; callers use them to locate tasks.

## Commands
`scala-cli run .`, `scala-cli test .`, `syntaxlab check`.
At the last stage, `scala-cli run . -- --interactive` starts the command loop.
After passing a stage, `syntaxlab check --checkpoint` explicitly requests a Git commit of the project and DB.
Related: [functions](functions.md), [collections](collections.md), [OOP](oop.md), [organization](organization.md).
