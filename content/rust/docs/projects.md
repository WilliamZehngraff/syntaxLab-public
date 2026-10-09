# Growing project · Task Trail

## Explanation
Extend one project in projects/rust/task-trail through ten stages. Keep Cargo.toml and accumulated tests; add your own source from scratch. The program grows from a banner to borrowed collection helpers, Task records, a Board interface, optional lookup, fallible parsing, module separation and a persistent CLI. Every library stage retains earlier helper APIs. The final CLI uses `list FILE`, `add FILE TITLE` and `done FILE ID`; no arguments retain the original banner. The project crate name is task_trail.

## Syntax and independent examples
```rust
// Independent command-line pattern:
fn main() {
    let arguments: Vec<String> = std::env::args().skip(1).collect();
    if let Some(name) = arguments.first() { println!("Hello, {name}"); }
}
// For failure: eprintln!("diagnostic"); std::process::exit(1);
```

## Common mistakes
- Keep a single project directory; switching stages does not replace source.
- Quote titles containing spaces at the shell.
- Distinguish missing files from malformed/unreadable existing files.
- Match Result at the CLI boundary rather than panicking on user input.
- Use syntaxlab check --checkpoint only when you explicitly want a Git commit.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [ownership](ownership.md), [structs](structs.md), [errors](errors.md), [file io](file-io.md), [testing](testing.md).
