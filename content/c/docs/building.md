# GCC and Make

## Explanation
Make describes targets and prerequisites. It rebuilds a target when a prerequisite has changed.
Compiler warnings highlight suspicious code; treat them as feedback rather than noise.

## Syntax and independent examples
```make
CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -Wpedantic -g
report: report.c report.h
	$(CC) $(CFLAGS) report.c -o report
.PHONY: clean
clean:
	rm -f report
```
Recipes require literal tabs. For larger projects, compile .c files to .o files and link the objects.

## Common mistakes
- A missing-separator error often means spaces were used instead of a tab.
- Put headers in prerequisites so a changed interface triggers rebuilding.
- -c compiles without linking; -o selects the output name; -g adds debugger information.

## Commands and related concepts
`make`, `make clean`, `make -n` (preview recipes). `gcc --version` reports your compiler.
Related: [organization](organization.md), [debugging](debugging.md), [projects](projects.md).
