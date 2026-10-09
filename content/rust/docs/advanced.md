# Generics and advanced ownership roadmap

**Roadmap:** this extension has no exercises yet and does not block the initial course.

## Explanation
Planned extensions: type parameters, trait bounds, explicit lifetimes, associated types, pattern guards, recursive enums, Box, Rc, RefCell, smart pointers, iterator implementations and error types. Start with ownership contracts and small trait interfaces before studying these abstractions.

## Syntax and independent examples
```rust
pub fn first<T>(values: &[T]) -> Option<&T> { values.first() }
```

## Common mistakes
- A lifetime annotation describes relationships; it does not extend a value's actual lifetime.
- Prefer a borrow when shared ownership is unnecessary.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [ownership](ownership.md), [structs](structs.md), [enums](enums.md).
