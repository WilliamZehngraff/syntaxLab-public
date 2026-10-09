# Pointers: addresses, indirection and ownership

## Explanation
A pointer stores an address, not the pointed-to value. & obtains the address of an object; unary * follows
an address. Types tell the compiler how to interpret the object and how far pointer arithmetic advances.
Passing a pointer by value copies the address, letting the callee access the same object.
Passing a pointer-to-pointer lets the callee replace the caller's pointer itself.

## Syntax and independent examples
```c
int count = 4;
int *position = &count;
*position += 2;                /* changes count */
int values[3] = {8, 9, 10};
const int *cursor = values;
int second = *(cursor + 1);
void forget(int **owner) { *owner = NULL; } /* needs stddef.h */
```
`p->field` abbreviates `(*p).field` for structs. `const int *p` forbids modifying the int through p;
`int *const p` forbids reassigning p. These are different promises.

## Common mistakes
- An uninitialized pointer does not point to valid storage.
- Never dereference NULL, a freed pointer, or a pointer to an expired local object.
- Pointer arithmetic is valid only within one array (plus its one-past position). Never dereference one-past.
- `int *a, b;` declares a pointer a and a plain int b. Prefer separate declarations.
- Null checks do not validate arbitrary addresses. Ownership and lifetimes are design responsibilities.
- Changing a local pointer does not change the caller's pointer; use an extra level of indirection when needed.

## Commands and related concepts
Run `python3 test_exercise.py`. For a crash, compile with -g and use `gdb ./program`, `run`, then `bt`.
AddressSanitizer (`-fsanitize=address,undefined`) can help expose invalid access on supported systems.
Related: [arrays](arrays.md), [structs](structs.md), [memory](memory.md), [debugging](debugging.md).
