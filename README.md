# C to Python Translator for While Statement

## Project description:
"C to Python Translator for While Statement" is a Python-based software tool designed to help translate C code into Python. 
The primary focus is on translating `while` loops, but the tool handles some other C constructs as well.

The tool uses the `pycparser` library to parse C code into an abstract syntax tree (AST), allowing us to analyze and understand the structure of the code. Additionally, `graphviz` is used to visualize these structures, particularly focusing on 'while' loops.
After parsing, the tool systematically translates C syntax into Python. The goal is to produce Python code that retains the logic and functionality of the original C code but leverages Python's syntax and features.
