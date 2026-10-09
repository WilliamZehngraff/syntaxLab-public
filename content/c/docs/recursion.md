# Recursion in C

## Explanation
A recursive call solves a smaller subproblem. A base case stops the calls. Each C call normally consumes
stack space, so a mathematically valid recurrence can still exhaust the stack. C does not guarantee
tail-call elimination. Use bounded inputs for these introductory exercises.

## Syntax and independent examples
```c
unsigned int power_two(unsigned int n) {
    if (n == 0) return 1;
    return 2 * power_two(n - 1);
}
```
For an array problem, reducing the length and advancing the pointer reduces the remaining structure.

## Common mistakes
- Check the base case before dereferencing an empty slice.
- A call with unchanged arguments never approaches termination.
- Multiplication may overflow before recursion runs out of stack; both limits matter.

## Commands and related concepts
Use `python3 test_exercise.py` and add base/one-step tests first.
Related: [functions](functions.md), [pointers](pointers.md), [arrays](arrays.md).
