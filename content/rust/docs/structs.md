# Structs, impl blocks and traits

## Explanation
A struct groups named fields. Visibility is explicit: a public struct can still have private fields. impl Type defines methods and associated functions. A conventional new constructor returns Self; &self inspects and &mut self changes an instance. A trait defines shared behavior, with required methods and optional defaults. Implementing a trait for a type supplies that contract without class inheritance.

## Syntax and independent examples
```rust
pub struct Meter { reading: i32 }
impl Meter {
    pub fn new(initial: i32) -> Self { Self { reading: initial } }
    pub fn value(&self) -> i32 { self.reading }
}
pub trait Printable {
    fn text(&self) -> String;
    fn print(&self) { println!("{}", self.text()); }
}
```

## Common mistakes
- new is a convention, not special constructor syntax.
- An associated function uses Type::function; an instance method uses value.method.
- Import a trait to use its methods through method-call syntax.
- Returning a borrowed field is safe; returning a reference to a temporary is not.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [ownership](ownership.md), [functions](functions.md), [enums](enums.md).
