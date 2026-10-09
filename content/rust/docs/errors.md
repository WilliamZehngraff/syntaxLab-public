# Result and recoverable errors

## Explanation
Result<T, E> carries Ok(value) or Err(error). Parsing and I/O commonly return Result. ? propagates an error from a function with a compatible result type; it does not panic. map_err converts the error representation. checked arithmetic returns Option for overflow, which can become Result with ok_or or ok_or_else. Reserve panic for broken assumptions, not ordinary invalid user input.

## Syntax and independent examples
```rust
pub fn read_score(text: &str) -> Result<i32, String> {
    let score = text.parse::<i32>().map_err(|_| "not an integer".to_owned())?;
    if score < 0 { return Err("negative score".to_owned()); }
    Ok(score)
}
```

## Common mistakes
- A valid parse may still violate the domain's range rules.
- ? can only be used where the enclosing function can return its error/absence type.
- Do not ignore Results from file operations.
- Avoid relying on debug-only overflow panics; use checked arithmetic for a fallible numeric contract.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [enums](enums.md), [file io](file-io.md), [testing](testing.md).
