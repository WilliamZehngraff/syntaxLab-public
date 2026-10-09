# Case classes, enums and optional values

## Explanation
Case classes are named records with value equality and copy. Enums describe a closed set of alternatives.
Option[A] represents a value that may be absent. Some(value) is present; None is absent. Prefer these over null.
Constructor patterns decompose case classes or Some just like tuple patterns.

## Syntax and independent examples
```scala
case class Contact(name: String, email: String)
val old = Contact("Jo", "old@example.test")
val updated = old.copy(email = "new@example.test")
enum Light:
  case Red, Amber, Green
def nameOf(contact: Option[Contact]): String = contact match
  case Some(Contact(name, _)) => name
  case None => "Anonymous"
```

## Common mistakes
- copy returns a new record, preserving fields you do not specify.
- Option.get throws on None. Match or use map/getOrElse instead.
- Do not use null to represent failure in a function returning Option.
- Closed alternatives let the compiler warn about missing cases.

## Commands and related concepts
Use `scala-cli test .` with both presence and absence.
Related: [OOP](oop.md), [pattern matching](pattern-matching.md), [error handling](error-handling.md).
