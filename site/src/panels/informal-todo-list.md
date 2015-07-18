---
template: mainpanel
source_form: markdown
name: Informal todo list
updated: July 2015
reviewed: 18 July 2015
title: Informal todo list
---
## Informal done list
* Statements are separated by NEWLINES
* Block structure generates INDENT/DEDENT tokens
* Value literals: Integers, String, Boolean
* Identifiers
* basic assignment statements - ie identifer equals expression
* function calls with expressions as arguments 
* print python 2 style statements
* expression statements
* expressions - specifically:
    * Those involving value literals, identifiers and function calls
    * Infix expressions involving * + / -
    * Parentheses ( ) for nested expressions.
* Arithemtic expressions for strings "+", "*", etc
* Loops - while / for
* forever_loop (while True)
* while takes an expression for the condition
* for takes an identifier for the iterator, and expression to be
   iterated over. The expression is treated as indexable thing with
   a length. A range() function call is detected and treated as a
   special case.
* If statements including elif and else clauses
* Can "import" C++ libraries - at least pre-processor directives work
* break / continue statements
* Partial comment support (check)
* Internals of implementation for generators (for implementing builtins first)

## Informal todo list

* Comments are started with a # character [*]   **[TBD]**
* function definitions with an optional argument list  **[TBD]**
* print replace as python 3 style statements  **[WIP]**
* Iterator version/expression of for_statement is tided up, and pluggable **[TBD]**
* parsing of yield statements   **[TBD]**
* parsing of import statements, parsing of from...import... statements   **[TBD]**
* Expressions - bitwise operators, logical operators, boolean operators   **[TBD]**
* Lists, list literals   **[TBD]**
* doc strings   **[TBD]**
* comments   **[TBD]**
* Dictionaries, dictionary literals   **[TBD]**
* Objects / object attribute access   **[TBD]**
* return statement   **[TBD]**
* The parser is line oriented, should be logical lines   **[TBD]**
* Lines are logical lines    **[TBD]**
 * ie Newlines are not yet suppressed.   **[TBD]**
 * Explicit line joining is not supported [2.1.5]    **[TBD]**
 * Implicitly line joining is not yet supported  [2.1.6]   **[TBD]**
* Generator implementation   **[TBD]**

