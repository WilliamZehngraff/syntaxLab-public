# Collections and transformations

## Explanation
A tuple holds a fixed number of potentially different types. A collection holds many values of a common type.
List supports efficient prepending and recursive decomposition. Vector supports efficient indexed access.
Seq describes an ordered sequence interface. Set removes duplicates. Map associates keys with values.
The default collections here are immutable: operations produce new collections. Mutable alternatives live in
scala.collection.mutable and require careful ownership of changing state.

## Syntax and independent examples
```scala
val pair: (String, Int) = ("Ada", 42)
val (name, score) = pair
val days = "Mon" :: "Tue" :: Nil
val values = Vector(4, 8, 12)
val changed = values.updated(0, 99)
val distinct = List(2, 2, 5).toSet
val ages = Map("Ada" -> 36)
val fallback = ages.getOrElse("Lin", 0)
val shortNames = List("Jo", "Alex").filter(s => s.length < 3).map(s => s.toUpperCase)
```

## Common mistakes
- Indices start at zero; invalid indexing throws.
- `xs.updated(...)` does not mutate xs. Use the returned collection.
- Sets have no meaningful positional order. Do not depend on their iteration order.
- A lambda `x => expression` is a function value, not immediate evaluation of that expression.

## Commands and related concepts
Run `scala-cli test .`; include empty collections and repeated elements.
Related: [functions](functions.md), [pattern matching](pattern-matching.md), [recursion](recursion.md).
