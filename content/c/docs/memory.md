# Heap storage and ownership

## Explanation
Automatic local objects usually live on the stack and expire when their scope ends. Heap allocations live
until explicitly freed. Give every allocation one clear owner; borrowed pointers must not outlive it.
malloc allocates uninitialized bytes; calloc allocates zero-initialized storage; realloc may move an allocation.

## Syntax and independent examples
```c
#include <stdlib.h>
int *items = malloc(6 * sizeof *items);
if (items == NULL) { /* handle failure before use */ }
else {
    int *resized = realloc(items, 12 * sizeof *items);
    if (resized != NULL) items = resized;
    free(items);
    items = NULL;
}
```
When realloc fails, the original pointer remains valid. After success the original pointer and its aliases
must no longer be used; use the returned pointer. New bytes are not automatically initialized.

## Common mistakes
- Returning a local array's address yields a dangling pointer.
- Losing the last owning pointer leaks an allocation.
- Freeing twice or accessing after free is undefined behavior.
- Check multiplication bounds before allocating for untrusted lengths; course contracts bound lengths.
- Setting one pointer to NULL does not fix other aliases to freed memory.

## Commands and related concepts
`python3 test_exercise.py`; optionally compile with -fsanitize=address,undefined -g for diagnostics.
Related: [pointers](pointers.md), [structs](structs.md), [projects](projects.md).
