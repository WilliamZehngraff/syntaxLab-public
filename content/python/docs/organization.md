# Modules, imports and lazy iteration

## Explanation
A module is a .py file; importing it executes its top-level statements once per process. Keep reusable calculations in modules and terminal I/O behind a main guard. A directory with __init__.py forms a regular package. Generators are functions containing yield: calling one creates an iterator; next or a for loop advances it. Use virtual environments for external dependencies, though this initial course needs only the standard library.

## Syntax and independent examples
```python
# util.py
def tidy(text: str) -> str:
    return text.strip()

# In another file: from util import tidy

def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

## Common mistakes
- Do not name your files json.py, unittest.py or other standard-library names.
- Avoid input() or print() during module import.
- An exhausted generator does not restart itself; create another iterator.
- Prefer explicit imports over wildcard imports.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [testing](testing.md), [file io](file-io.md).
