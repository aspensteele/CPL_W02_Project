CPL_W02_Project

Interpreter for a subset of the SCL (System Control Language) used in CS4308: Concepts of Programming Languages.

Created by:
Colin Haskins, Shamitha John, Aspen Steele, Aashna Suthar

Project Overview

This project implements a simple end-to-end interpreter:

Scanner (Python) → Token JSON
Parser (Python) → Parse Tree JSON
Executor (Java) → Runs the program

How to Run
1. Scanner (Python)

Converts .scl source → *_tokens.json

python scl_scanner.py example.scl

2. Parser (Python)

Converts token JSON → *_parse_tree.json

python parser.py example_tokens.json

3. Executor (Java)

Runs the parse tree and creates an automatic output file
(e.g., example_parse_tree_output.txt)

Compile:

javac -cp .;json-simple-1.1.1.jar Executor.java


Run:

java -cp .;json-simple-1.1.1.jar Executor example_parse_tree.json

Example SCL Program
int x = 5;
int y = 10;
x = x + y;

if (x > 10) {
    y = y + 1;
} else {
    y = y - 1;
}

What Each Component Supports

Scanner: integers, identifiers, keywords (int, if, else, while), operators
Parser: declarations, assignments, if/else, while, expressions
Executor: arithmetic, conditions, blocks, variable memory, output logging
