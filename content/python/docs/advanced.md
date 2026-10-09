# Advanced Python roadmap

**Roadmap:** this extension has no exercises yet and does not block the initial course.

## Explanation
Planned extensions after the initial course: comprehensions over nested data, decorators, context-manager protocols, typing.Protocol, generics, packaging with pyproject.toml, logging, property-based testing and more advanced data models. Start by mastering explicit interfaces and deterministic tests.

## Syntax and independent examples
```python
from typing import Protocol

class HasName(Protocol):
    def name(self) -> str: ...
```

## Common mistakes
- Type annotations are not runtime validation.
- Prefer a direct function until an abstraction removes real duplication.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [oop](oop.md), [organization](organization.md), [testing](testing.md).
