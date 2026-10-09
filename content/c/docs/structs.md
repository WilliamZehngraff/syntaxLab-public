# Structs and shared types

## Explanation
A struct groups named fields. typedef introduces a convenient type name. Passing a struct by value copies it;
passing its pointer allows modifications to the original. Put shared type definitions in guarded headers.

## Syntax and independent examples
```c
typedef struct { int x; int y; } Point;
Point p = {.x = 2, .y = 5};
int horizontal = p.x;
void move(Point *point, int dx) { point->x += dx; }
```

## Common mistakes
- Use . on a struct value and -> on a pointer to a struct.
- A typedef definition ends with a semicolon.
- Do not define incompatible copies of a shared struct in different files; include one header.
- Copying a struct containing pointers copies addresses, not the pointed-to allocations.

## Commands and related concepts
Compile with warnings; run `python3 test_exercise.py`.
Related: [pointers](pointers.md), [organization](organization.md), [projects](projects.md).
