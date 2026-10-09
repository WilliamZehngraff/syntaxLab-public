# Strings and capacity

## Explanation
A C string is a sequence of chars followed by a zero byte, '\0'. Its storage must include that extra byte.
Length excludes the terminator; capacity includes all available bytes. Functions need both a pointer and a
capacity to write safely. String literals must not be modified; use char arrays for writable storage.

## Syntax and independent examples
```c
#include <string.h>
#include <stdio.h>
char name[12] = "Lin";
size_t length = strlen(name);
int equal = strcmp(name, "Lin") == 0;
char message[32];
snprintf(message, sizeof message, "Hi %s", name);
```
snprintf returns the number of characters it wanted to write (excluding '\0'); compare this with capacity
to detect truncation. strcpy assumes enough room; avoid it unless you have proved the capacity.

## Common mistakes
- '0' is a visible digit; '\0' is a zero byte.
- `a == b` compares pointers, not string contents.
- Filling all capacity bytes with visible text leaves no terminator.
- Reading beyond a terminator or writing beyond capacity invokes undefined behavior.

## Commands and related concepts
`python3 test_exercise.py`; test empty, exact-fit, one-byte and too-small destinations.
Related: [arrays](arrays.md), [pointers](pointers.md), [structs](structs.md).
