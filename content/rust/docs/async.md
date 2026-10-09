# Async Rust roadmap

**Roadmap:** this extension has no exercises yet and does not block the initial course.

## Explanation
Planned extensions: futures, async/await, executors, cancellation and asynchronous I/O after the synchronous fundamentals. No async runtime or external crate is required by the initial course.

## Syntax and independent examples
```rust
pub async fn answer() -> u32 { 42 }
// A future needs an executor to drive it; creating it alone does not run it.
```

## Common mistakes
- async does not automatically mean parallel execution.
- Avoid blocking an executor thread with synchronous work.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [ownership](ownership.md), [errors](errors.md), [organization](organization.md).
