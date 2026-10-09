# Headers and compilation units

## Explanation
A header shares declarations. A .c file defines functions. Each .c compiles separately; the linker resolves
calls across object files. Include guards prevent duplicate declarations of types within one compilation unit.

## Syntax and independent examples
```c
/* counts.h */
#ifndef COUNTS_H
#define COUNTS_H
int next_count(int current);
#endif
/* counts.c includes "counts.h" and defines next_count. */
```
Use quotes for local headers and angle brackets for standard library headers.

## Common mistakes
- Do not include a .c file; compile and link it instead.
- Avoid non-static function definitions in headers, which can cause duplicate symbols.
- Undefined references indicate missing definitions or missing object files at link time.

## Commands and related concepts
`gcc -Wall -Wextra -Wpedantic -c counts.c` then link objects with the main object's file.
Related: [functions](functions.md), [building](building.md), [structs](structs.md).
