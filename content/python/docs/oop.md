# Classes, dataclasses and inheritance

## Explanation
A class defines a type with data and behavior. __init__ initializes an instance; self identifies the current instance. Store independent state on self rather than in shared class attributes. Dataclasses generate initialization and equality for records; frozen=True prevents ordinary field reassignment. Inheritance can share behavior that calls methods overridden by a subclass. Prefer small interfaces over deep hierarchies.

## Syntax and independent examples
```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Contact:
    name: str
    email: str

old = Contact("Jo", "old@example.test")
new = replace(old, email="new@example.test")

class Meter:
    def __init__(self, initial=0):
        self._reading = initial
    def advance(self, amount):
        self._reading += amount
```

## Common mistakes
- A leading underscore marks an internal detail by convention; it is not enforced privacy.
- A mutable class-level list is shared across instances.
- Defining __init__ does not remove the need to pass self in method definitions.
- A frozen record can still refer to a mutable nested object; choose field types carefully.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [collections](collections.md), [organization](organization.md).
