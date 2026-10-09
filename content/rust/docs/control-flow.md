# Rust decisions, loops and ranges

## Explanation
An if expression produces a value; its branches must have compatible types. Conditions must be bool. for iterates over a range or collection; a..b excludes b and a..=b includes it. while checks a condition before each iteration; loop repeats until a break. continue advances to the next iteration, while break exits the nearest loop. A loop can return a value with break value.

## Syntax and independent examples
```rust
pub fn sign(n: i32) -> &'static str {
    if n < 0 { "negative" } else { "nonnegative" }
}
// Inside a function:
// for day in 1..4 { println!("Day {day}"); }
// let mut fuel = 3;
// while fuel > 0 { fuel -= 1; }
```

## Common mistakes
- Numeric zero is not a substitute for false.
- A loop body must make progress toward its stop condition.
- Check range endpoints explicitly.
- Do not add a semicolon to a branch's final expression when its value is needed.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [functions](functions.md), [collections](collections.md), [projects](projects.md).
