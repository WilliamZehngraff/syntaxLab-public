# Rust functions and library interfaces

## Explanation
Functions declare each parameter type and an optional -> result type. The final expression supplies the result if it has no semicolon. A semicolon discards that expression's value; a function with no interesting result returns unit (). Integration tests compile as separate crates, so the tested library API must be public. Rust has no default/named function arguments or same-name overloads; use explicit functions, tuples or configuration structs instead.

## Syntax and independent examples
```rust
pub fn offset(value: i32, amount: i32) -> i32 {
    value + amount
}

// In src/main.rs, call syntaxlab_exercise::offset(9, 4).
```

## Common mistakes
- Missing pub makes a function inaccessible to integration tests.
- A trailing semicolon can turn an intended integer result into ().
- Rust does not silently mix incompatible numeric types.
- Keep printing at the binary boundary when callers need a calculated value.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [foundations](foundations.md), [control flow](control-flow.md), [organization](organization.md).
