# Exceptions, parsing and absent values

## Explanation
Exceptions separate failure from normal return values. Raise a specific exception when a contract cannot be fulfilled; catch narrowly at a boundary that can recover or report. None can represent expected absence. Validation is distinct from parsing: successfully reading an integer does not prove it lies in the valid domain. The | type annotation expresses alternatives such as int | None.

## Syntax and independent examples
```python
def read_score(text: str) -> int | None:
    try:
        number = int(text)
    except ValueError:
        return None
    if number < 0:
        raise ValueError("negative score")
    return number
```

## Common mistakes
- Bare except catches too much, including exceptions you did not intend to suppress.
- Do not substitute zero for every error when zero is a valid result.
- Use is None to check absence.
- assert is a debugging/testing tool, not reliable validation of user input under python -O.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [file io](file-io.md), [testing](testing.md).
