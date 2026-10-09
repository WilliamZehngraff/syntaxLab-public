# Pattern matching

## Explanation
Match decomposes a value by shape. Cases run top-to-bottom; the first applicable case wins.
Constants compare values, variable patterns bind names, `_` discards a value, and guards add conditions.

## Syntax and independent examples
```scala
def axis(p: (Int, Int)): String = p match
  case (_, 0) => "horizontal"
  case (0, _) => "vertical"
  case (x, y) if x > y => "below diagonal"
  case _ => "elsewhere"
def firstOrZero(xs: List[Int]): Int = xs match
  case Nil => 0
  case head :: tail => head
```

## Common mistakes
- A lowercase name in a pattern binds a new variable; it is not a constant comparison.
- Put general cases after specific cases or they hide them.
- Handle every shape. Compiler exhaustivity warnings are valuable.
- `h :: t` matches a nonempty list; t may itself be empty.

## Commands and related concepts
Test each case with `scala-cli test .`, especially an unmatched input.
Related: [collections](collections.md), [recursion](recursion.md), [data modeling](data-modeling.md).
