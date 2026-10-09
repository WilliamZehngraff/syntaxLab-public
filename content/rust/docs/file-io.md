# Paths, UTF-8 and file failures

## Explanation
std::path::Path borrows a path and PathBuf owns one. std::fs::read_to_string and write manage file handles and return io::Result. read_to_string requires valid UTF-8. ? propagates opening, reading and writing failures to a caller that can report them. For persistence, serialize fields rather than memory addresses and validate every loaded record before treating it as domain data.

## Syntax and independent examples
```rust
use std::{fs, io, path::Path};

pub fn copy_note(from: &Path, to: &Path) -> io::Result<()> {
    let text = fs::read_to_string(from)?;
    fs::write(to, text)
}
```

## Common mistakes
- A missing file is different from an unreadable existing file.
- write replaces contents; the caller must choose a deliberate path.
- Error messages should retain enough context to identify the failed operation.
- Test with temporary paths and clean up rather than relying on personal files.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [errors](errors.md), [organization](organization.md), [projects](projects.md).
