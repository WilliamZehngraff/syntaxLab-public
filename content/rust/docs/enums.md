# Enums, match and Option

## Explanation
Enums express a closed set of alternatives, optionally carrying data. match must cover every possibility. Patterns bind values or ignore them with _. Option<T> represents expected absence using Some(value) and None. Derive can generate standard traits such as Debug, Clone and PartialEq when the fields support them. Use explicit data types instead of sentinel values that could also be legitimate results.

## Syntax and independent examples
```rust
#[derive(Debug, PartialEq)]
pub enum Status { Waiting, Finished }

pub fn describe(value: Option<i32>) -> String {
    match value {
        Some(n) => format!("value {n}"),
        None => "missing".to_owned(),
    }
}
```

## Common mistakes
- Qualify variants with their enum type unless imported.
- unwrap on None panics; handle absence at the appropriate boundary.
- Put broad wildcard cases after specific ones.
- Deriving Copy is only possible when every contained value is Copy.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [structs](structs.md), [errors](errors.md), [collections](collections.md).
