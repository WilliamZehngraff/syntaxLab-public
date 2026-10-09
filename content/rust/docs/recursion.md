# Recursive numbers and borrowed structures

## Explanation
A recursive function solves a smaller version of the same problem. A base case ends the chain; every recursive step must approach it. A borrowed subslice gives a smaller structural problem without allocating new storage. Rust does not guarantee tail-call elimination. Bound depth and numeric range separately: stack overflow and integer overflow are different failures.

## Syntax and independent examples
```rust
pub fn power_two(n: u32) -> u64 {
    if n == 0 { 1 } else { 2 * power_two(n - 1) }
}
```

## Common mistakes
- Check the base case before indexing a possibly empty slice.
- Unchanged recursive arguments never reach termination.
- Choose a wide enough result type before multiplication.
- Deep production traversals may need an explicit stack.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [functions](functions.md), [ownership](ownership.md), [testing](testing.md).
