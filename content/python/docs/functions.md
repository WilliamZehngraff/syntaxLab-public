# Python functions and scope

## Explanation
def names a reusable calculation. Parameters are local names bound to passed objects; return sends a result to the caller. A function without an explicit return produces None. Local helpers belong to one calculation. Keyword arguments use parameter names; defaults are evaluated once when the definition runs. Keep input/output in the entry point so tests can import the module without executing the application.

## Syntax and independent examples
```python
def offset(value: int, amount: int = 2) -> int:
    return value + amount

if __name__ == "__main__":
    print(offset(amount=4, value=9))
```

## Common mistakes
- Printing is not returning.
- Avoid mutable default values such as items=[]; use None and create a new list inside the call.
- Assignment inside a function normally creates a local name; avoid hidden global state.
- The main guard distinguishes direct execution from import.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [foundations](foundations.md), [control flow](control-flow.md), [organization](organization.md).
