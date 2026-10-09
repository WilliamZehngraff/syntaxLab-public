# Concurrency roadmap

**Roadmap:** this extension has no exercises yet and does not block the initial course.

## Explanation
Planned extensions: threads, move closures, channels, Arc, Mutex, Send/Sync and deterministic coordination. Ownership provides compile-time help but does not remove the need to design ordering and failure handling. The initial course does not spawn learner threads.

## Syntax and independent examples
```rust
// A thread owns the captured message.
// let message = String::from("worker");
// let handle = std::thread::spawn(move || println!("{message}"));
// handle.join().unwrap();
```

## Common mistakes
- Shared ownership is not the same as synchronized mutation.
- Joining or communicating is necessary when completion order matters.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [ownership](ownership.md), [errors](errors.md), [testing](testing.md).
