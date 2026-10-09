# Arrays and dimensions

## Explanation
An array stores contiguous elements of one type. Its indices begin at zero. Passing an array to a function
normally passes a pointer to its first element; its length must travel separately.
Multidimensional arrays are arrays of rows. The compiler needs the inner dimensions for address calculations.

## Syntax and independent examples
```c
int scores[4] = {10, 20, 30, 40};
void clear(int values[], int length) {
    for (int i = 0; i < length; ++i) { values[i] = 0; }
}
int board[2][3] = {{1, 2, 3}, {4, 5, 6}};
```
const int values[] expresses read-only access through that parameter. It does not copy the array.

## Common mistakes
- C performs no automatic bounds checks.
- sizeof on an array parameter measures a pointer, not the caller's array.
- Do not dereference anything for a zero-length input.
- A local fixed array cannot be safely returned as a pointer: its lifetime ends at return.

## Commands and related concepts
Run `python3 test_exercise.py` with empty, singleton and multi-element cases.
Related: [strings](strings.md), [pointers](pointers.md), [memory](memory.md).
