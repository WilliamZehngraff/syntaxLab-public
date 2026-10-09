# Vec, maps, sets and iterator transformations

## Explanation
Vec<T> owns a growable sequence. iter borrows its elements, iter_mut lends mutable references and into_iter consumes the collection. Iterator adapters such as map and filter are lazy; collect chooses the destination collection. Closures use |parameters| expression syntax. HashMap associates keys with values; entry(key).or_insert(default) lends mutable access to a value. HashSet represents uniqueness. Neither hash collection promises iteration order. get returns Option, introduced fully in the enum module.

## Syntax and independent examples
```rust
use std::collections::{HashMap, HashSet};

fn main() {
    let numbers = vec![4, 8, 12];
    let shifted: Vec<i32> = numbers.iter().map(|n| n + 1).collect();
    let mut counts: HashMap<String, usize> = HashMap::new();
    *counts.entry("note".to_owned()).or_insert(0) += 1;
    let unique: HashSet<i32> = shifted.into_iter().collect();
    println!("{}", unique.len());
}
```

## Common mistakes
- collect often needs a destination type annotation.
- A closure's parameter may itself be a reference; read compiler types carefully.
- Do not rely on map/set order; sort when output order is part of the contract.
- Borrow the input if the caller must retain it.

## Commands
```sh
cargo run
cargo test
syntaxlab check
```

Related: [ownership](ownership.md), [enums](enums.md), [functions](functions.md).
