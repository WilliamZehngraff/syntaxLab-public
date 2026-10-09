# Python recursion

## Explanation
A recursive function solves a smaller instance of its own problem. A base case ends the calls; the recursive step must reduce the remaining problem. Numeric recursion reduces a number; structural recursion follows a list or tree. Python has a recursion depth limit and does not optimize tail calls, so deep production traversals usually need iteration or an explicit stack.

## Syntax and independent examples
```python
def power_two(n: int) -> int:
    if n == 0:
        return 1
    return 2 * power_two(n - 1)
```

## Common mistakes
- Missing the base case or reusing unchanged arguments causes runaway recursion.
- Check an empty list before reading its first item.
- Slicing a list copies elements; repeated recursive slicing can be expensive.
- Do not increase the recursion limit as a substitute for reasoning about termination.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [collections](collections.md), [testing](testing.md).
