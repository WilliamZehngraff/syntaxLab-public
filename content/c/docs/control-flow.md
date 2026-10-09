# C control flow

## Explanation
if/else selects statements. switch chooses integer/enum cases. Loops repeat work; distinguish a condition
tested before the body (while/for) from one tested after it (do/while).

## Syntax and independent examples
```c
if (score >= 50) { puts("pass"); } else { puts("retry"); }
switch (mode) {
    case 0: puts("quiet"); break;
    case 1: puts("verbose"); break;
    default: puts("unknown"); break;
}
for (int i = 0; i < 4; ++i) { printf("%d\n", i); }
while (remaining > 0) { --remaining; }
do { ++attempts; } while (attempts < 1);
```
break leaves the nearest loop/switch; continue starts the next iteration of the nearest loop.

## Common mistakes
- A stray semicolon after an if or while creates an empty body.
- switch falls through unless you break or return intentionally.
- Use `< length` for zero-based elements; `<= length` accesses one too many.
- The do/while statement needs its final semicolon.

## Commands and related concepts
Compile with `gcc -Wall -Wextra -Wpedantic`; run `python3 test_exercise.py`.
Related: [foundations](foundations.md), [functions](functions.md), [arrays](arrays.md).
