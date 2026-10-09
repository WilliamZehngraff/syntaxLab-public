# Recursion: from numbers to structure

## Explanation
A recursive function solves a smaller version of its own problem. Identify a base case and a step that
strictly reduces the input. Numeric recursion reduces a number; structural recursion follows a data shape.
Ordinary recursion remembers pending work on the stack. An accumulator carries that work as a parameter.
When the recursive call is the final operation, `@tailrec` can verify stack-safe compilation.

## Syntax and independent examples
```scala
def powerOfTwo(n: Int): Long =
  if n == 0 then 1L else 2L * powerOfTwo(n - 1)
def lastOrZero(xs: List[Int]): Int = xs match
  case Nil => 0
  case x :: Nil => x
  case _ :: tail => lastOrZero(tail)
```
For tail recursion, import `scala.annotation.tailrec`, annotate a helper, and pass the answer-so-far.
`1 + recurse(...)` is not tail-recursive: addition is still waiting when the call returns.

## Common mistakes
- Missing the empty or zero case causes unbounded recursion.
- Recursing on the original input makes no progress.
- Reversing construction order reverses a List. Follow the contract's order.
- A tailrec error means there is pending work; do not remove the annotation to hide it.
- Numeric result overflow is distinct from stack overflow; choose Long where needed.

## Commands and related concepts
Use `scala-cli test .`; check base, one-step, multiple-step and large inputs separately.
Related: [functions](functions.md), [pattern matching](pattern-matching.md), [recursive data](recursive-data.md).
