---
template: mainpage
source_form: markdown
name: Changelog
title: Changelog
updated: August 2015
---
## Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/), within
reason.

### In progress

## [0.0.17] - UNRELEASED

### New

* Implemented "pass" statement
* For loops now work on arduino profile (reimplemented C++ generators to use
  generator state, not to use an exception)
* Arduino test case using for loop

### Other

* Extracted core code for "pyxie" script into pyxie.core
* Updated usage instructions to include covering using arduino profile

## [0.0.16] - 2015-08-02

Summary: Adds initial Arduino LEONARDO support, improved function call, release build scripts

In particular, to compile for a compilation target you do this:

pyxie --profile arduino some_program.pyxie

This will generate some_program.hex. You then need to load this onto your
arduino. Support for assisting with this will probably be in a largert
version. Requires Arduino.mk to be installed in a standard place. Docs TBD
as functionality stabilises.

### Features

* Arduino LEONARDO compatible compilation profile (#3)
  * Detect that we are in a profile mode from a command line switch (#3.1)
  * Code generation is called with current profile (#3.2)
  * Code generation outputs code targetting "setup" instead of "main" (#3.3)
  * Makefile uses the arduino makefile #arduino leonardo (#3.4)
* Compilation profiles support removal of elements of the clib (#4.1)

* Function calls that do not require arguments work (#2)

### Docs

* Docs in README.md, setup.py and docs/ are generated from website. (#66)
* Documentation in /docs is generated from website source documentation (#63)
* Docs on usage #docs (#64)
* Man page for pyxie (#65)

### Other

* Make Release Script (#61)
* build_release_script.py (#62)
* Core setup.py files/etc now auto-generated from templates

### Other

* Clean up build local script
* Man file added (not installed yet though)
* Build distributed docs from the same source as the website
* Added pyxie-dev script to assist in release automation
* Re-enable doc building


## [0.0.15] - 2015-07-18

* clib converted to py clib for adding to build directory

## [0.0.14] - 2015-07-18

### New

* clib - this will be a collection of C++ code that can be directly or indirectly used in  generated programs. Current focus is iterators
* C++ generator support - to support C++ iterators
* C++ generator implemention of python's range iterator + acceptance test harness
* Lex/Parsing of For
* Type inference/analysis for special cased iterator functions
* Pynode representation of for loops
* Code generation for for loops using iterators

### Other

* Extra test case for while - testing 3 way logical expressions
* Test case for for loops
* Massive website revamp

## [0.0.13] - 2015-06-21

This probably marks the first release that's potentially properly useful when combined with
an appropriate included .h file... We support if/elif/else while/break/continue and arbitray
expressions.

### New

* Support for if statements
* Support for elif clauses (as many as desired)
* Support for else clauses
* Support for boolean operators - specifically and/or/not, including any mixture
* Support for parenthesised expressions

## [0.0.12] - 2015-06-17

### New

* Initial iteration of website - hosted at www.sparkslabs.com/pyxie/ . Stored in repo
* support for while statements:
 * While works with While True
 * Break works with With True
 * 'Continue' works in a While loop
 * While Loop conditional is a expression
  * This allows things like loops that count towards zero and do things... :-)
* Comparison Operators :  < > <= >= <> != ==

Combination of these things allows things like countdown programs, basic
benchmarking and so on. Creative use ( while + break) allows creation of "if" like
constructs meaning the code at this point supports sequence, selection and iteration
as well as very basic datatypes. That's almost useful... :-)

## [0.0.11] - 2015-06-06

### New

* Function call support:
 * Extended Grammar, and pynodes to support function calls.
 * Code generation for function calls
 * Test cases for function calls added
 * Creation of  "Print" built in for the moment- to be replaced by 'print'
* C++ "bridge":
 * Create simple C++ include bridging - #includes are copied straight through
 * Document C++ bridging, and test case

### Changed

* Language Spec updates

### Fixes

* Support empty statements/empty lines

## [0.0.10] - 2015-06-03

* Documentation added to pyxie/__init__.py, to allow project level help from "pydoc pyxie"
* Expression Statements
* Improved type inference in explicit analysis phase 
 * Explicit analysis phase added - decorates AST, focussed on types. Results of this phase viewable.
 * Pynodes are now tree nodes, simplifying tree traversal for common cases
 * Variables are managed by contexts -- context is added to pynodes during analysis phase, simplifying type inference
 * Contexts changes to store name and list of expressions -- not name and identifier, again, simplifying and generalising type inference
 * Ensure all identifies in global context *before* analysis starts, simplifying analysis phase
 * New strategy for type inference documented, opens up lexical scoping
* pyxie compile harness now runs/compiles programs outside the pyxie tree

## [0.0.9] - 2015-05-23

Primary changes are to how the program is run, and fixes to precedence. This is the first
version to support a non-test mode - so you can output binaries, but also JSON parse trees.

### New
* Test modes for pyxie harness moved into a --test mode
* Standalone parse mode -- pyxie parse filename -- parses the given filename, outputs result to console
* Standalone compiler mode --
 * pyxie compile path/to/filename.suffix -- compiles the given file to path/to/filename
 * pyxie compile path/to/filename.suffix path/to/other/filename -- compiles the given file to the destination filename

### Changed
* Switch to left recursion. The reason is because YACC style grammars handle
  this better than right recursion, and the fact it also fixes operator precedence
  correctly in expressions. The reason the grammar was originally right recursive
  is because that's the Grammar that CPython uses, but the parsing process must
  be different (since it's LL(1) and suitable for top down rather than bottom up
  parsing)

### Fixes
* Bracket negative literal values in expressions to avoid confusing C++
* Precedence as noted above.

## [0.0.8] - 2015-05-13
### Changed
Switched compilation over to using PyNode objects rather than lists

Rolls up alot of changes, and improvements:

* Simple test case for testing expressions in assignments
* Added release date for 0.0.7
* Bump revisions for next release
* Use PyNodes to represent python programs
  In particular, this replaces the use of lists with the use of objects.
  The aim here is to simplify type inference from code, and injection of
  context - like scoping - into the tree to be able to infer types and
  usage thereof.

* We're doing this at this stage because the language is complex enough for
  it to start to be useful, but simple enough for it to be not too difficult
  to switch over to.

  Furthermore, by allowing nodes to generate a JSON representation, it's easier
  to see the actual structure being generated - to allow  tree simplification,
  but also to allow - at least temporarily - decoupling of changes from the
  python parsing from the C tree generation, and from the C code generation

* Clean up statements node creation in grammar
* Simplify expression lists
* Support iterating over statements
* Transform pynodes to CST lists for assignment
* Reverse number order to not match line numbers
* Iterate over expressions within an expr_list
* Convert assignments from pynodes
* Remove old code
* Can now transform basic core programs based on pynodes
* Code generation for expressions as rvalues
* Better test for code generation of expression rvalues
* Add context into pyidentifier nodes
* Support transforms for expression rvalues in assignment
* First pass at adding context - variable lookups into the system
* Test case that derives types for variables



## [0.0.7] - 2015-04-29
### Changed
- Bump revision for release
- Compiler structure & testing improvements
- Initial support for infix integer addition expressions
- Support for plus/minus/times/divide infix operations
- Add test regarding adding string variables together
- Make parser more relaxed about source file not ending with a newline
- Bugfix: Fix precedence for plus/minus/times/divide
- Bugfix: Only output each include once

## [0.0.6] - 2015-04-26
Overview -- Character Literals, math expressions, build/test improvements
### Changed
- Character literals - parsing and compilation
- Initial version of changelog
- Mark WIP/TBD, add character
 - Adds character type, mark which bits of the spec are now TBD, and which are WIP
- Add "in progress" section to CHANGELOG
- Build lexer explicitly
- Basic mathematical expression parsing
 - Parsing of basic expressions involving basic mathematical operators, as opposed to just value_literals.
- Test case for parsing mathematical expressions
- Allow parser to be reset
- Restructure test harness to allow more selective testing
  This also changes the test harness to be closer to a standard
  compiler style API.
- Run all tests from makefile
- Codegen test for basic math expressions
  Simplest possible test initially


## [0.0.5] - 2015-04-23
### Added
- Core lexical analysis now matches language spec - collection of changes, which can be summarised as follows:
 - Language spec updated relative to implementation & lexing states
 - Lexical analysis of block structure
 - Lexical analysis of operators, punctuation, numerical negation
 - Implement numbers part of the grammar (including negation), including basic tests
 - Fleshed out lexical tokens to match language spec

### Changed
- Code cleanups

## [0.0.4] - 2015-04-22
### Added
- Extends C AST to match python AST semantics
- Ability to use mixed literals in a print statement (1,True, "hello" etc)
- Argument list management
- Convert argument lists explicitly

### Changed
- Use Print not print

### Fixed
- Cleaned up debug output.

## [0.0.3] - 2015-04-21
### Added
- Adds ability to print and work with a small number of variables
- Better handling, and code gneration for integer literals

### Changed
- Add long description (setup.py)
- Update README.md to reflect project slightly better
- Reworded/tightened up README
- Updated documentation
- Emphasise "yet" when saying what it does (README)
- Zap the source between compilation runs
- Build test results inside the test-data/genprogs directory


## [0.0.2] - 2015-03-30

*Initial Release*

Simple assignment

### Added
- Transform Python AST to C CST - compile python to C++ for v simple program

### Changed
- Various tweaks for README/docs
- Packaging for pypi and Ubuntu Launchpad PPA for initial release 0.0.2

## [0.0.1] - Unreleased - rolled into 0.0.2
### Added

- Initial structure, loosely based on SWP from a few years ago
 - http://www.slideshare.net/kamaelian/swp-a-generic-language-parser
- Initial pyxie parsing/model/codegen modules
- Basic parsing of value literals, decorated with source information
- Support for basic identifiers and assignment including simple type inference
- First pass at a simple C++ code generator for concrete C++ AST
- Directories to hold semantic models and for code generation
- Represent C programs as json, and allow construction from json
- Simple program that matches the C++ code generator
