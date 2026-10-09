# Functions

## Explanation
A function gives a calculation a name. Parameters are its inputs; its declared result type is its contract.
The last expression is returned. A pure function depends only on its inputs and changes no outside state.
Local helpers hide details that belong to one operation. Overloads share a name but differ in parameter types.
Recursion builds on functions in the dedicated [recursion module](recursion.md).

## Syntax and independent examples
```scala
def offset(value: Int, amount: Int): Int = value + amount
def caption(text: String, prefix: String = "Note"): String = s"$prefix: $text"
val note = caption(prefix = "Tip", text = "Save often")
def surround(s: String): String =
  def bracket(t: String): String = s"[$t]"
  bracket(s)
def describe(n: Int): String = s"number $n"
def describe(s: String): String = s"text $s"
```

## Common mistakes
- Give each parameter its own type; multiple parameters are comma-separated.
- `def f(): Unit` promises effects, not a numeric return value.
- A default is declared once, at the definition. Named arguments use the parameter's actual name.
- Changing only a return type does not create a valid overload.
- Do not print inside a function whose caller needs the calculated value.

## Commands and related concepts
Run `scala-cli test .` after adding a function, then `scala-cli run .` for your demo.
Related: [foundations](foundations.md), [control flow](control-flow.md), [collections](collections.md).
