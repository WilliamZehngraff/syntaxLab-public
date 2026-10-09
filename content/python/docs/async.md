# Concurrency and async roadmap

**Roadmap:** this extension has no exercises yet and does not block the initial course.

## Explanation
Planned extensions: iterators versus asynchronous iterators, async/await, asyncio tasks, cancellation, thread/process tradeoffs and resource ownership during concurrent work. The initial course has no asynchronous exercises or network dependencies.

## Syntax and independent examples
```python
import asyncio

async def pause():
    await asyncio.sleep(0)

# asyncio.run(pause()) runs an async entry point.
```

## Common mistakes
- Calling an async function creates a coroutine; it does not run it to completion.
- Do not block an event loop with long synchronous work.

## Commands
```sh
python3 main.py
python3 -m unittest discover -s tests -v
syntaxlab check
```

Related: [organization](organization.md), [errors](errors.md), [testing](testing.md).
