# C foundations

## Explanation
C source is text in .c files. The preprocessor handles #include; the compiler creates object code;
the linker joins object files and libraries into an executable. A successful compile does not run it.
main is the entry point and returns a status to the shell: zero means success.

## Syntax and independent examples
```c
#include <stdio.h>
int main(void) {
    const int hours = 4;
    double rate = 2.5;
    char unit = 'h';
    /* Formats must match the arguments. */
    printf("%d %c at %.1f\n", hours, unit, rate);
    return 0;
}
```
`short`, `int`, `long`, `long long` are integer types; widths depend on the platform.
`unsigned` types represent nonnegative values; signed overflow is undefined. `sizeof(type)` reports bytes.
`float` and `double` approximate real numbers. Use LL for long long literals, f for float.
Use %d for int, %u for unsigned, %ld for long, %lld for long long, %c for char, %f for floating values,
%zu for size_t. float arguments are promoted to double in printf.
`+ - * / %` calculate; `== != < <= > >=` compare; `&& || !` are logical operators.

## Common mistakes
- A missing semicolon may cause an error on the following line.
- `=` assigns; `==` compares. `&` is not logical AND.
- `7 / 2` is integer division; cast an operand before dividing for a fractional result.
- Char literals use single quotes; strings use double quotes and escape sequences such as \n and \t.

## Commands
```sh
gcc -std=c17 -Wall -Wextra -Wpedantic main.c -o program
./program
python3 test_exercise.py
syntaxlab check
```
The visible verifier adds -Werror so warnings must be addressed, not hidden.
Related: [functions](functions.md), [control flow](control-flow.md), [building](building.md).
