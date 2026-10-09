# Lists, dictionaries, sets and tuples

## Explanation
Lists are mutable ordered sequences. A slice creates a shallow copy; assignment creates another reference to the same object. Dictionaries associate hashable keys with values and preserve insertion order. Sets represent uniqueness, not positional order. Tuples group a fixed set of values and cannot be reassigned element-by-element. A shallow copy still shares nested mutable objects.

## Syntax and independent examples
```python
values = [4, 8, 12]
copy = values[:] 
copy.append(16)
ages = {"Ada": 36}
fallback = ages.get("Lin", 0)
unique = set([2, 2, 5])
ordered = sorted(unique)
name, score = ("Jo", 42)
for index, value in enumerate(values):
    print(index, value)
```

## Common mistakes
- list.reverse and list.sort mutate and return None; reversed/sorted have different interfaces.
- Indexing starts at zero; invalid indices raise IndexError.
- dict[key] raises KeyError when absent; get can provide a fallback.
- Do not depend on set iteration order in output or tests.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [control flow](control-flow.md), [oop](oop.md).
