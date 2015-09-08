---
template: mainpage
source_form: markdown
name: Language Status
updated: August 2015
reviewed: 12 August 2015
title: Language Status for Pyxie
---
## Language Status

Last updated for version: **0.0.17**

{% compilation = panel("panels/direct-compilation.md") %}

## Example program that lexes, parses, analyses & compiles

Clearly a single example doesn't tell you everything. This gives you a flavour.

{% exampleprogram = panel("panels/example-program.md") %}

Supported language features that are not in this example

* Major control structures - in addition to while loops, if/elif/else, conditionals,
  boolean, parenthesised expressions and for statements/etc are all supported. Not
  only that for loops actually support an iterator protocol, not just translation of
  "range" into a simple C style for loop.

Note: for this to compile, this needs simple type inference. We need to be able to
derive the types of foobar and new_age_three. In the case of new_age_three, that
needs to be derived in the context of another variable that has to be derived from
another one.

The same techniques are used to derive types in "for statement" loop iterators.

### Function Calls

Function **calls** are supported. At present they are treated
as having a value type of "None".  They should be treated as statements
not as expressions. However the compiler passes through function calls
to the backend, assuming the backend will understand the function call.

Grammar wise though, they're things in expressions.

### C++ Libraries

Additionally, you can pull C++ libraries in standard locations by simply
incuding them -- for example:

    #include <Arduino.h>

This is ignored by the python parsing because it's a comment, and so I've
chosen to capture such #include lines, and pass them through to the C++ side.
This naturally enables a wide selection of functionality to start making
Pyxie useful.

### Very Nearly Bare Minimum Support

Now supports control structures, key statements

* while (arbitrary expression for control)
* for loops, where the general expression must be an iterable.
 * The only iterable at present is "range". This will get more expressive
* break/continue
* if/ elif / else
* print
* function calls
* assignment

Key expression support:

* Variables have their types inferred for int, bool, char, float, string, hex, binary, octal
* Parenthesised expressions
* Comparisons (>,<,>=,<=, !=,<>, ==)
* Boolean operators: and, or, not

This means we can almost start writing useful programs, but in particular
can start creating simplistic benchmarks for measuring run speed.

## High Level things missing

### Language related

From a high level the key things I view as missing are support for:

* def - function definitions - and therefore implementation of scope
* What happens with mixed types in expressions
* Modulo operator support
* import statements
* yield - generator definitions
* class - class definitions
* object usage - method access, and attribute access

There is obviously more missing, but these are the high level issues with pyxie's
implementation of language at present.

### Profile related

* Linux host profile:
 * Support for output (print) needs to be matched by (raw_)input support
 * Needs to support input/output from files

* Arduino profile:
 * Need to support the following things at minimum:
 * Constants:
  * OUTPUT, INPUT (pinModes)
  * HIGH, LOW (general pin values)
 * functions/etc
  * digitalWrite
  * delayMicroseconds
  * pinMode
  * analogRead
  * millis
 * Hardware devices/libraries etc
  * Servo
  * IOToy
  * prototype microbit

## Grammar Currently Supported

Clearly we're not going to implement the full language spec in one go, so this
documents the current version of the grammar that is supported. Parsing does not
necessarily imply code generation, differences will be noted below.

{% grammar = panel("panels/current-grammar.md") %}

The lexing supports most aspects of python - much more than this, but the grammar
does not as yet use them, so this summary does not list them.

{% grammar = panel("panels/limitations.md") %}

{% grammar = panel("panels/why-python-2-print.md") %}

## Compilation process strategy

The compiler consists of the following parts:

* A lexical analyser. This is a simple parse with 3 modes. These modes are essentially:
  * NORMAL - this is used most of the time and is regular parsing
  * BLOCKS - entered at end of line, and used to check whether to start/finish a BLOCK
  * ENDBLOCKS - this is used to close off 1 or more blocks

* A grammar parser - this constructs an abstract syntax tree for the python code. This
  uses Pynodes - which form a tree. This process does as little as possible beyond
  building the tree - however it aims to throw away as little information as possible.

* Pynodes - these are used to capture information in the abstract tree, and to assist
  with analysis. These are standard tree nodes (now), but can perform custom traversals
  for specific tasks.

* Analysis Phase - WIP. This performs the following tasks:
  * Works down through the AST, DEPTH FIRST, adding context to identifier nodes. This
    is to allow type identification/capture.
    * This idea here is that if you pass into an AST node that represents a syntactic
      scoped namespace - such as a function, class/etc, that we can stack the scopes
      with regard to names, values and especially types

  * Open issues:
    * We need logical values of some kind to be avilable for use in contexts, to be
      referenced by identifiers. Logical values are values that can be assigned or
      read at a specific point in time. In traditional terms this are literally
      represented as expressions, but it's a bit more subtle than that - we want to
      represent expression results.

    * Working down through the AST currently trees the AST as a flat tree - in terms
      of namespaces - a single global one. To determine scoping rules we need to be
      able to differentiate where a tree/subtree starts/finishes in a traversal.
       * Probably requires a custom traversal to be honest

  * The analysis phase decorates the AST with additional data

* Code generation phase:
  * Takes a JSON description from the AST and uses that to create a C-Syntax Tree.
    This syntax tree kinda mirrors the sort of tree that you'd expect to get out
    of the semantic analysis phases of a simplistic C compiler.
  * This is then walked to generate simple C++ code

* Compilation
  * The next step is to take the generated code and compile it. For the moment, this
    operates on the code generated, and compiles it as a linux standalone. This will
    switch over to allowing arduino as a target at some point.

Analysis phase now picks up on the use of a variable before it's definition in code.
This is the start of useful error states and therefore useful error messages!

## Type inference strategy

Create the node tree.

**DONE**

* Traverse down the tree adding a context object to all identifiers. **DONE**

**WIP**

* Then when we do types, we search inside the object and set it inside the object. **DONE**

**TBD**

* When you pass through a class or def, you push the current one onto a stack and refer to it as the parent context **TBD**

* We repeat this until all the types of variables are *known* **TBD** (def/class still TBD)

* If any are unknown we stop type inference. **TBD**

It's simple, but should work and has stopping criteria.

And can build on what we have now

Before we do that though, let's fix the code generation for identifiers, since it's gone screwy!

