# Paths, UTF-8 and JSON

## Explanation
pathlib models paths independently of manual slash concatenation. Always state the text encoding when storing portable data. with closes a file even when an exception occurs; Path.read_text/write_text provide convenient managed operations. JSON stores data, not executable code. Validate its decoded shape before constructing your domain objects. Let callers choose paths; avoid writing files merely because a module was imported.

## Syntax and independent examples
```python
import json
from pathlib import Path

path = Path("notes.json")
path.write_text(json.dumps({"topic": "café"}, ensure_ascii=False), encoding="utf-8")
record = json.loads(path.read_text(encoding="utf-8"))
with Path("notes.txt").open(encoding="utf-8") as stream:
    for line in stream:
        print(line.rstrip("\n"))
```

## Common mistakes
- Missing files, permission errors and malformed data are separate failure paths.
- Opening with w replaces existing content; choose the path deliberately.
- A valid JSON document may still have the wrong fields/types.
- Use tempfile.TemporaryDirectory for tests instead of depending on a personal file.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [errors](errors.md), [organization](organization.md), [projects](projects.md).
