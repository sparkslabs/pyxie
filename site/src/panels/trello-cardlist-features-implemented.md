---
template: mainpanel
source_form: markdown
name: Trello Cardlist Features Implemented
updated: July 2015
title: Trello Cardlist Features Implemented
---
### Features Implemented

* 0.0.15 = = = = = = = = = =
* BUG: clibs can only be used on development machine...
* 0.0.14 = = = = = = = = = =
* BUG: statement_block at EOF not emitting dedents correctly #fixed
* Simple for...range loops
* Function call code supports simplified type definitions for builtins (such as range)
* Compile phase is split into "codegen" and "compile"
* Implement a simple iterator protocol for C++ objects - to allow implementation of something like range functions and generators.
* Implementation of a simple C Library to include into user generated code as necessary.
* 0.0.13 = = = = = = = = = =
* Parsing bracketed full expressions
* Chained boolean expressions and chained mixtures of boolean expressions work as expected
* Boolean expression support: NOT
* Boolean expression support: AND
* Boolean expression support: OR
* Support for if/elif/else statements
* Support for if statements
* 0.0.12 = = = = = = = = = =
* Release tasks: 0.0.12
* Comparison operators
* Can now handle loops that count towards zero and do something with them...
* support for while statements
* While Loop conditional is a expression
* Continue works in a While loop
* Break works with With True
* While works with While True:
* Define basic principles for Pyxie
* 0.0.11 = = = = = = = = = =
* Function call code generation supports Print as special case
* Code generation function calls
* Support python comments so we can CHEAT and do things like #include <arduino.h> :-D (What a *neat* idea :-) )
* Parsing function calls
* 0.0.10 = = = = = = = = = =
* Pyxie will now compile files outside the pyxie code tree
* Code generation of expression statements.
* Test suite checks that programs that should fail to compile do so
* Test suite uses new analysis hook
* PARSING USES STANDARD TREE MODEL, BUT ALSO USES CUSTOM TRAVERSALS FOR FLEXIBILITY
* Type inference code changes are refactored and cleaned up
* Strategy for managing variables needs defining
* New strategy for type inference - lexical scope friendly
* Analysis through tree for identifiers doesn't work as expected. Needs fixing/resolving
* Now, before we analyse types, all identifiers are guaranteed to be in the global context. We don't need to stuff in a new version, just update it.
* Contexts themselves are kinda wrong, need a rethink
* Analysis Phase adds context
* Pynodes are tree nodes (and hence trees)
* Analyse is an explicit phase internally, initially focussed on types
* Results of analyse phase can be made visible.
* Docs added to pyxie/__init__.py
* 0.0.9 = = = = = = = = = =
* Pyxie harness supports parsing random files
* Pyxie harness supports compiling random files
* Pyxie harness has a testing mode
* Bracket negative literal values in expressions to avoid confusing C++
* Pyxie is now left recursive not right recursive
* conversion of expression statements
* BUG: 10-1-2 gives 9 not 11
* 0.0.8 = = = = = = = = = =
* Replace python AST list style representation with a nodal representation - to simplify type decoration etc
* Type inference for expressions
* assignment where the rvalue is a simple integer expression
* Variable types are looked upin/stored to  a global context.
* Testcase added for assignments where the rvalue is an expression
* BUGFIX: Should only include iostream once, if at all.
* Printing of op_func blocks
* Conversion of core "operator functions" for integers
* Code generation for INTEGER core expressions
* BUGFIX: Precedence for operators is inverted for some reason.  +- binding tighter than */
* BUG - When the parser is reused, line numbers in lexer do not reset for new files
* Parsing core expressions - times, divide, power, plus, minus  - NOT function call, not parenthesised
* Parsing blocks generates block tokens
* Lexical Analysis matches initial language spec
* Print handles mixed literals
* Code generation for atomic literals
* "models" contains an initial baseline model mapping python-CST to CPP-CST
* Generation of decorated CPP-CST from parsed assignment statements
* C++ Code can be generated from the baseline CPP-CST for libc based testing
* Parsing assignment statements
* Parsing identifiers
* Parsing of value literals
* Baseline parser/lexer infrastructure for parser build/testing
* Long description on PyPI
