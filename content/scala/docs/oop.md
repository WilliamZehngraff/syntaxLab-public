# Classes, constructors and interfaces

## Explanation
A class describes instances with data and behavior. The primary constructor is declared in the class header.
Plain parameters are available during construction; val/var parameters also expose fields. Prefer val.
An auxiliary constructor delegates to the primary one. A companion object is a singleton with the same name
as its class and can expose factories. A trait specifies reusable behavior and required operations.

## Syntax and independent examples
```scala
class Meter(val unit: String, initial: Int):
  private var reading = initial
  def this(unit: String) = this(unit, 0)
  def value: Int = reading
  def advance(amount: Int): Unit = reading += amount
object Meter:
  def empty: Meter = new Meter("steps")
trait Printable:
  def text: String
  def print(): Unit = println(text)
class Note(val text: String) extends Printable
```
Methods called through a trait reference use the concrete object's implementation: polymorphism.
Overriding a concrete member uses `override`. Advanced inheritance, abstract classes and trait composition
are planned in [advanced OOP](advanced-oop.md); prefer small interfaces to deep hierarchies.

## Common mistakes
- Local variables in a method disappear after that call; fields belong to an instance.
- A public var exposes unrestricted mutation. Prefer a private field with explicit operations.
- Auxiliary constructors begin with `this(...)`, not arbitrary statements.
- Two instances should not accidentally share mutable state in a companion object.

## Commands and related concepts
Run `scala-cli test .` with two instances to test independence.
Related: [functions](functions.md), [data modeling](data-modeling.md), [organization](organization.md).
