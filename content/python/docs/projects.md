# Growing project · Study Planner

## Explanation
Build one persistent CLI over ten stages in projects/python/study-planner. Early stages establish output and pure helpers; later stages add collections, dataclasses, a Planner class, optional lookup, validated JSON, separate modules and argparse. New stages add tests without replacing your source. Keep earlier helper APIs callable from main.py even after moving implementation to planner.py; explicit imports can preserve that interface. The final app has add/list/done commands and an explicit data-file argument.

## Syntax and independent examples
```python
# Independent argparse example, not the project implementation:
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
print(f"Hello, {args.name}")
```

## Common mistakes
- Do not start a new directory at each stage; extend the existing program.
- Do not use a mutable default list for every Planner instance.
- Reject malformed persisted records rather than silently discarding them.
- Free-form titles are one quoted shell argument.
- After passing a stage, syntaxlab check --checkpoint explicitly requests a Git checkpoint.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [oop](oop.md), [errors](errors.md), [file io](file-io.md), [testing](testing.md).
