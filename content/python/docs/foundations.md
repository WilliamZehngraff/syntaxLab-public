# Python foundations

## Explanation
Python executes .py text files through an interpreter. Statements normally end at a newline; indentation groups blocks. A name refers to an object and may be rebound. int represents arbitrary-sized integers; float approximates real numbers; str stores Unicode text; bool has True and False. None represents absence. Comments begin with #. input reads one text line; print writes values followed by a newline. Type annotations describe intent but do not enforce types at runtime.

## Syntax and independent examples
```python
city = "Oslo"
degrees = 8
degrees += 2
print(f"{city}: {degrees} C")
ratio = 5 / 4       # 1.25
whole = 5 // 4      # 1
remainder = 5 % 4   # 1
enabled = True
print(enabled and degrees >= 0)
text = "  Notes  ".strip()
print(text.lower(), len(text))
```

## Common mistakes
- = assigns; == compares. Use and/or/not for logic.
- / differs from //, and int truncation differs from floor division for negative values.
- String methods return new strings; they do not change the original.
- input always returns str; convert deliberately when a number is required.
- Use spaces consistently rather than mixing tabs and spaces.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [control flow](control-flow.md).
