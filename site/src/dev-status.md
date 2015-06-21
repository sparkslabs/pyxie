---
template: mainpage
source_form: markdown
name: Dev Status
updated:  Thu Jun 18 16:12:42 2015
title: Detailed Dev status
---
## Trello dump for Pyxie
(auto extracted)
###  Project Stage

* HEADLINE: PRE-ALPHA
* DEV STATE: MAKE IT WORK
* DEV VERSION: 0.0.14
* RELEASED: 0.0.13
* LANGUAGE STATE: PRE-BARE
* How to deploy the website
* Release tasks


###  TODO: Website, docs, etc

* Man page for Pyxie
* Docs on usage
* Blog post: Introducing Pyxie
* Blog post: Pyxie structure
* Blog Post: Pyxie Decisions
* Start thoughts on pyxie-web
* Start thoughts on pyxie-gui


###  TODO: Tasks

* Link current test programs on the website, maybe
* Pyxie compile harness is switched over to use a better system for determining runtime options
* Review whether context should check types of ALL expressions, rather than just first, and whether we can should try to detect type mismatches
* https://travis-ci.org/
* Review pypi packaging for things we should be doing
* Create pyxie-service for managing batch compilation services
* Add the manpage to the distributed files, into the right places
* Add updating man page to the makefile


###  Arising and Internal

* Truthiness for values that AND/OR/NOT arguments needs resolving properly in C. (deferred)
* Truthiness of expressions is explicitly checked/valid - for us in if and while statements and boolean expressions
* Website could do with some pictures :-)
* Should we allow comments on website?
* Can find_variables(AST) in pyxie.model.transform actually just look in the results of the analysis phase? It should be able to. Building the same structure after all
* Code generation of C literals is muddled up a touch with structural representation
* C Syntax Tree is a Tree
* Currently have 2 shift/reduce conflicts. They're auto-resolved correctly, but could be worth seeing if they could be resolved better.
* Consider using CppHeaderParser on the C++ side of things - to inform the code generation side of things
* Block structure of generated C Code is pretty/human friednly/readable
* Operations and operators could be unified with a bit of tweaking - using "x.operation", not "x.tag/x.comparison" etc
* Better Error messages for users
* Duplication exists within code generation for operators. (cf convert_operator etc)


###  TODO: Features

* Unify Boolean operator pynode implementations
* Comments are implemented - would be useful for documented tests more appropriately
* Arduino compatible compilation mode.
* MBed compatible compilation mode?
* MSP430 compatible compilation mode?
* Add special case for function calls like print...
* Generalise special casing of function calls.
* Variables inside while loops are handled correctly
* Function call code supports simplified type definition files.
* Core expression code generation for strings
* Implement container oriented comparison operators
* Implement identity oriented comparison operators
* Support for for statements
* Code generation for integer literals retains original representation where possible (Octal, hex, binary, etc)
* Function call code supports C style function prototypes for type definitions
* Function call code supports name C headers for type definitions
* Pyxie caches results of C style header parsing
* Modulo Operator for Strings
* Modulo Operator for Integers
* Modulo Operator for Floats


###  Next

* Bump Versions
* For Release: 0.0.14
* Simple for...range loops
* Pyxie compile harness supports custom working directories


###  Known Bugs / Anti-features

* 5: Website should use responsive CSS
* 5: Website side bar could be better implemented.


###  Tasks Next Release



###  Features Next Release



###  WIP



###  Features Implemented

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


###  Tasks Done

* 0.0.13 - - - - - (tasks)
* For Release: 0.0.13
* Decide on Python Modulo operator?
* Bump Versions
* 0.0.12 - - - - - (tasks)
* Update language status for 0.0.12
* BUG: Parser generates far too many "empty statements"
* Update language status for 0.0.11
* Check docs in pyxie/__init__.py match 0.0.12 Release
* Bump Versions
* Push rebased site to github/live
* Site for Pyxie, should link to language spec -- http://www.sparkslabs.com/Pyxie/language-spec.md
* 0.0.11 - - - - - (tasks)
* For release: 0.0.11
* Check docs in pyxie/__init__.py match 0.0.11 Release
* Bump Versions
* 0.0.10 - - - - - (tasks)
* For release: 0.0.10
* Check that programs that compile produce expected code
* Check docs in pyxie/__init__.py match 0.0.10 Release
* Update test target in makefile to match new pyxie args
* Bump Versions
* Order of functions in pynode matches grammar - making it easier to follow
* Document current parsing status more accurately
* 0.0.9 - - - - - (tasks)
* Check that debian package being built/created does actually contains what's wanted
* Check that the tar ball being built/created for pypi actually contains what you want
* Version number bumped
* 0.0.8 - - - - - (tasks earlier)
* Why the project doesn't use the standard python compiler/AST module
* Break down language features into specific feature tasks - for initial feature set
* pyxie compiler now accepts runtime options to control what tests get compiled
* Changelog for initial releases
* Initial language spec
* Packaging for pypi exists
* Packaging via PPA exists
* The CST for baseline Python code is simplified
* Initial testing infrastructure in place
* Private github repo for Pyxie
* initial README for Pyxie
* Pyxie 0.0.1 Released
* Pyxie 0.0.2 Released
* Pyxies 0.0.3 Released
* Pyxie 0.0.4 Released
* Pyxie 0.0.5 Released


###  Pinned

* Things to feed into Pyxie
* Licensing links
* .p files are parsing tests. If they compile, they should be renamed .pyxie which are compilation tests.


###  Rejected



###  Inbound



