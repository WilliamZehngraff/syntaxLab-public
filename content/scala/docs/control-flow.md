# Control flow

## Explanation
`if` selects a value; a while loop repeats effects until its condition becomes false.
A for loop visits a collection or range; for/yield constructs a collection of results.
Branches are evaluated only when selected. Keep mutation local to the calculation that owns it.

## Syntax and independent examples
```scala
def sign(n: Int): String = if n < 0 then "negative" else "nonnegative"
var fuel = 3
while fuel > 0 do
  println(fuel)
  fuel -= 1
for day <- 1 until 4 do println(s"Day $day")
val shifted: Seq[Int] = for n <- 0 to 3 yield n + 10
```

## Common mistakes
- `to` includes the endpoint; `until` excludes it.
- A while body must eventually change the condition or terminate.
- An if used as a value needs compatible types in both branches.
- for/do prints or changes things; for/yield produces values. They are not interchangeable.

## Commands and related concepts
Use `scala-cli test .` with zero, one, and boundary-sized inputs.
Related: [functions](functions.md), [collections](collections.md), [pattern matching](pattern-matching.md).
