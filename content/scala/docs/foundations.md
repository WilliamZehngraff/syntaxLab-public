# Scala foundations

## Explanation
Scala source lives in `.scala` text files. Scala CLI compiles them and runs an entry point.
`project.scala` contains `//> using` directives: these configure Scala 3 and the test dependency.
A value is an expression's result. `val` binds once; `var` can be reassigned. Prefer val.
The initial lessons cover both supported entry styles, every basic value type, and operators.

## Syntax and independent examples
```scala
@main def weather(): Unit =
  val city: String = "Oslo"
  var degrees = 8                 // inferred Int
  degrees += 2
  println(s"$city: $degrees C")

// Alternative entry style (use one entry point per early exercise):
object Main:
  def main(args: Array[String]): Unit = println("A new day")

val large: Long = 9000000000L
val fraction: Float = 0.25f
val precise: Double = 5.0 / 4
val letter: Char = 'Q'
val enabled: Boolean = true
val truncated: Int = precise.toInt
val valid = enabled && truncated >= 0
```
`Unit` means no interesting result, as with println. `+ - * / %` are arithmetic operators;
`== != < <= > >=` compare values; `&& || !` combine/invert Booleans. Parentheses control grouping.
Strings use double quotes; Char uses single quotes. In interpolation `${expression}` handles calculations.

## Common mistakes
- Integer division happens before conversion: `(5 / 2).toDouble` is 2.0, not 2.5.
- Assignment is `=`; equality is `==`.
- Scala 3 indentation groups statements. Align sibling lines and indent bodies.
- Writing a val is not printing it. Call println to see it in the terminal.

## Commands
```sh
scala-cli run .
scala-cli test .
syntaxlab check
```
First test execution downloads pinned artifacts; subsequent runs use the local cache.
Related: [functions](functions.md), [control flow](control-flow.md), [project organization](organization.md).
