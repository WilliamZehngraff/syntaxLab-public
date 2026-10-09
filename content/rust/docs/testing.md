# Cargo tests and deterministic properties

## Explanation
cargo test compiles the real library/binary and runs functions annotated #[test]. Integration tests in tests/ use public crate APIs. assert_eq! reports expected/actual values; assert! checks a predicate. Test boundaries, empty inputs, invalid data and independent state. Fixed loops over inputs illustrate property thinking without a new framework. The course has no crates.io dependencies, so cargo test --offline works once Rust is installed.

## Syntax and independent examples
```rust
#[test]
fn addition_identity() {
    for n in -20..=20 { assert_eq!(n + 0, n); }
}
```

## Common mistakes
- Code must compile before any test can run.
- Printing a value is not a test assertion.
- Do not rely on test order or shared mutable global state.
- unwrap is useful in a test where failure should fail that test; it is not an error-handling strategy for a CLI.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [functions](functions.md), [errors](errors.md), [organization](organization.md).
