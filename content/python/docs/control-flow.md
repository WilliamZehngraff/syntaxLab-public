# Python decisions and iteration

## Explanation
if/elif/else chooses statements. Conditions use truthiness: zero, empty collections, empty strings and None are false-like. for iterates over values; range produces a sequence of integers without building a list. while repeats as long as a condition remains true. break exits a loop; continue starts its next iteration. Comprehensions build collections from iteration and optional filtering.

## Syntax and independent examples
```python
def sign(n: int) -> str:
    if n < 0:
        return "negative"
    return "nonnegative"

for day in range(1, 4):
    print(day)
lengths = [len(name) for name in ["Jo", "Alex"] if len(name) > 2]
fuel = 3
while fuel > 0:
    fuel -= 1
```

## Common mistakes
- range's stop is excluded.
- A while loop must make progress toward termination.
- Put statements at the right indentation level, especially return after a loop.
- Filter before a transformation if that transformation loses information needed by the filter.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [collections](collections.md), [projects](projects.md).
