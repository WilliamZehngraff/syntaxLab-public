# Rust foundations and Cargo

## Explanation
Rust compiles source into native executables. Cargo manages a package described by Cargo.toml: src/main.rs is the binary entry point and src/lib.rs defines a reusable library. fn main() starts a binary. let bindings are immutable unless declared mut. Signed/unsigned integers have fixed widths; usize is used for lengths/indices. f32/f64 approximate real values; bool is true/false. char stores one Unicode scalar value, &str borrows UTF-8 text, and String owns a growable UTF-8 buffer. The course uses Rust 2021 and no external crates; stable Rust 1.70+ is sufficient.

## Syntax and independent examples
```rust
fn main() {
    let city = "Oslo";
    let mut temperature: i32 = 8;
    temperature += 2;
    println!("{city}: {temperature} C");
    let ratio = 5 as f64 / 4 as f64;
    let (label, number) = ("day", 3);
    let values = [10, 20, 30];
    println!("{ratio} {label} {number} {}", values[0]);
}
```

## Common mistakes
- println! is a macro; keep the !.
- = assigns; == compares; &&/||/! are Boolean operators.
- Array indices begin at zero and out-of-bounds access panics.
- Integer division discards the fractional part before a later cast.
- Cargo may create Cargo.lock; keep it in Git for reproducible binary projects. target/ is a cache.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [functions](functions.md), [ownership](ownership.md).
