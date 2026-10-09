# Python tests and deterministic contracts

## Explanation
unittest is part of Python's standard library. TestCase methods beginning with test_ are discovered by the supplied command. Test returned values, boundaries, exceptions, independence of objects and absence of unintended side effects. Use fixed inputs and temporary directories; avoid relying on the clock, network, random state or test execution order.

## Syntax and independent examples
```python
import unittest

class ArithmeticTests(unittest.TestCase):
    def test_identity(self):
        for n in range(-20, 21):
            self.assertEqual(n + 0, n)
    def test_bad_integer(self):
        with self.assertRaises(ValueError):
            int("not a number")
```

## Common mistakes
- Printing a value does not make a test fail.
- Test file names must start with test_ for default discovery.
- A test should assert an observable contract, not duplicate every implementation step.
- Keep learner modules import-safe so discovery does not wait for interactive input.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [functions](functions.md), [errors](errors.md), [organization](organization.md).
