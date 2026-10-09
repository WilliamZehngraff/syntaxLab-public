# File I/O and error paths

## Explanation
fopen creates a FILE stream or returns NULL. Read/write operations can fail independently of opening.
Close every stream you successfully open, including on error paths. Parsing should not corrupt existing
state when input is invalid. File persistence is an explicit operation, not a side effect of every edit.

## Syntax and independent examples
```c
FILE *stream = fopen("notes.txt", "r");
if (stream != NULL) {
    char line[80];
    if (fgets(line, sizeof line, stream) != NULL) { puts(line); }
    if (fclose(stream) != 0) { /* report failure */ }
}
```
`r` reads existing files, `w` truncates/creates, `a` appends. fscanf reports the count of successful conversions;
fprintf reports characters written or a negative error. fclose can report buffered-write failures.

## Common mistakes
- Never pass a NULL FILE pointer into reading/writing functions.
- Do not loop on feof before attempting a read; inspect the read's return value.
- Treat a malformed file as a failure path, not valid zero data.

## Commands and related concepts
Run `python3 test_exercise.py`; use disposable paths for tests.
Related: [strings](strings.md), [pointers](pointers.md), [projects](projects.md).
