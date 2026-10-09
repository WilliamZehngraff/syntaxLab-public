# Project organization

## Explanation
Scala CLI compiles the source tree beneath the directory you give it. Split responsibilities into files.
Packages name logical groups; imports bring names into scope. project.scala holds pinned directives.
Tests ending `.test.scala` have test scope and run with MUnit under `scala-cli test .`.

## Syntax and independent examples
```scala
// util/Text.scala
package util
object Text:
  def tidy(s: String): String = s.trim
// Another file:
// import util.Text
```
Dependency syntax: `//> using dep "group::artifact:version"`; test-only dependencies use `test.dep`.
The double colon selects the Scala binary version. The initial course needs no sbt.

## Common mistakes
- A file name does not automatically create a package.
- Keep one clear application entry point; multiple @main methods require --main-class selection.
- Do not put reference implementations in test files.

## Commands and related concepts
`scala-cli run .`, `scala-cli test .`, `scala-cli compile .`.
Related: [testing](testing.md), [OOP](oop.md), [projects](projects.md).
