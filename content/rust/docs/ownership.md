# Ownership, moves, borrowing and slices

## Explanation
Each owned value has an owner; when it goes out of scope its resources are dropped. Moving a String transfers ownership, while simple Copy values such as i32 are copied. &T borrows shared access; &mut T borrows exclusive access. While a borrow is active, Rust enforces either shared reads or exclusive mutation. Slices borrow contiguous elements and carry a length. &str is a string slice; strings cannot be indexed by arbitrary byte offsets as if each byte were a character.

## Syntax and independent examples
```rust
pub fn announce(text: &str) { println!("Note: {text}"); }
pub fn extend(text: &mut String) { text.push_str("..."); }

fn main() {
    let mut message = String::from("Start");
    announce(&message);
    extend(&mut message);
    println!("{message}");
    let values = [1, 2, 3];
    let tail: &[i32] = &values[1..];
    println!("{}", tail.len());
}
```

## Common mistakes
- Do not clone merely to silence every ownership error; first choose the intended ownership contract.
- &mut requires the caller's binding to permit mutation.
- Never return a reference to a local value that will be dropped.
- String.len counts UTF-8 bytes, not characters; chars counts scalar values, not grapheme clusters.
- Multiple aliases cannot mutate simultaneously.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [functions](functions.md), [collections](collections.md), [structs](structs.md).
