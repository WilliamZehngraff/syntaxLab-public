# Growing project · Task Ledger

## One workspace, fifteen stages
Task Ledger starts as a printed banner, then grows counters, decisions, arrays, strings, structs, pointer
operations, heap storage, a multi-file build, and file persistence. The final CLI loads, adds, lists and
completes tasks in a local text file. All stages reuse projects/c/task-ledger.
Keep previous APIs working: the accumulated test harnesses are your regression suite.

## Design and independent example
Write the simplest version first. Separate storage operations from the terminal interface.
```c
/* A small borrowed-output contract, unrelated to task storage: */
int read_mode(const char *text, int *mode); /* 1 on success, 0 without modification on failure */
```
Borrowed pointers do not transfer ownership. Heap buffers have explicit owners; every successful allocation
must eventually be freed. Save only in response to explicit commands.

## Common mistakes
- Do not reset the directory between stages; extend your program.
- Keep test_*.c harnesses out of the application link; each has its own main.
- Do not store raw pointer addresses in a persistence file. Serialize fields as text.
- Check file and allocation errors before dereferencing anything.

## Command-line input (final stage)
An entry point may receive arguments as `int main(int argc, char **argv)`.
argc counts the strings, including the program name at argv[0]. User arguments start at argv[1].
Check argc before indexing argv. Quoting in the shell keeps a title with spaces in one argument.
For example, an unrelated greeting tool could use:
```c
int main(int argc, char **argv) {
    if (argc != 2) { fputs("Provide one name\n", stderr); return 1; }
    printf("Hello, %s\n", argv[1]);
    return 0;
}
```
Include stdio.h for those I/O functions. Use strcmp to compare command names. For numeric arguments,
strtol from stdlib.h reports the first unparsed character through its end-pointer parameter; check
that some digits were consumed, no suffix remains, errno is not ERANGE, and the value fits the
contract's range. Unlike atoi, this permits reporting invalid input. argc/argv are borrowed storage:
do not free them. Review [strings](strings.md), [pointers](pointers.md), and [file I/O](file-io.md).

## Commands
`python3 test_01.py` (and each added stage script), `syntaxlab check`, then `make` after the build stage.
Final usage: `./program list tasks.txt`, `./program add tasks.txt 'Read a book'`, `./program done tasks.txt 1`.
Use `syntaxlab check --checkpoint` to explicitly request a Git stage checkpoint.
Related: [functions](functions.md), [pointers](pointers.md), [memory](memory.md), [file I/O](file-io.md).
