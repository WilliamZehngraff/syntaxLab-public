# Cargo layout, modules and re-exports

## Explanation
A Cargo package can contain a library and a binary. mod text declares a module usually stored in text.rs or text/mod.rs; use brings a name into scope. pub use re-exports a name as part of the public API. Modules control visibility and responsibility, not textual inclusion. Integration tests in tests/*.rs import the library by its crate name. Cargo.lock records resolved versions; target/ is disposable build output.

## Syntax and independent examples
```rust
// src/lib.rs
mod formatting;
pub use formatting::tidy;

// src/formatting.rs
// pub fn tidy(text: &str) -> String { text.trim().to_owned() }

// src/main.rs calls syntaxlab_exercise::tidy(...)
```

## Common mistakes
- A source file is not compiled as a module unless declared.
- Hyphens in package names become underscores in crate import names.
- Keep implementation details private while exposing tested interfaces.
- Do not put another main in an integration test; #[test] marks test functions.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [functions](functions.md), [structs](structs.md), [testing](testing.md).
