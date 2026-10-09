# Testing and properties

## Explanation
A test is executable evidence for a contract. Examples cover chosen inputs; properties describe classes
of inputs. Deterministic checks are repeatable: use fixed inputs or fixed seeds, never the current clock.

## Syntax and independent examples
```scala
class ArithmeticTests extends munit.FunSuite:
  test("addition identity") {
    for n <- -20 to 20 do assertEquals(n + 0, n)
  }
```

## Common mistakes
- A passing example does not prove correctness for every input.
- Test boundaries, empty values, and repeated calls, not only the happy path.
- An assertion tests a result. Printing a value alone does not fail a test.
- Avoid tests that merely copy the implementation's exact steps.

## Commands and related concepts
`scala-cli test .` discovers MUnit tests. Compiler errors occur before any tests run.
Related: [functions](functions.md), [organization](organization.md), [recursion](recursion.md).
