# C functions and scope

## Explanation
A declaration describes a function's signature; a definition supplies its body. Parameters are passed by
value: a function receives copies. To modify caller-owned data, pass a pointer (later lessons).
Automatic local variables belong to one call. File-scope static functions are private to that compilation unit.

## Syntax and independent examples
```c
int offset(int value, int amount);   /* prototype */
static int twice(int n) { return n * 2; }
int offset(int value, int amount) { return value + amount; }
```
Use void as the parameter list for a function taking no arguments, and as the result type for no returned value.
C functions cannot be nested. Reuse helpers instead of repeating calculations.

## Common mistakes
- A prototype needs types even when parameter names are omitted.
- A non-void function must return a result on every path.
- Printing is not returning. Callers cannot calculate with a printed line.
- A declaration must be visible before a call; headers share declarations across files.

## Commands and related concepts
`python3 test_exercise.py` compiles your application and then links your functions into a test harness.
Related: [pointers](pointers.md), [recursion](recursion.md), [organization](organization.md).
