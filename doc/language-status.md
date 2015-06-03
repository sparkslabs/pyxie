# Language Status

Pyxie can now compile (directly) any file that matches pyxie's current subset of
python. For example if the example program below was called demo.pyxie, you could
do this:

    $ pyxie compile demo.pyxie
    $ ./demo

The first line would compile "demo.pyxie" to C++, then compile the C++, rename the
result "demo" and clean up after itself.

## Example program that lexes, parses, analyses & compiles

Clearly a single example doesn't tell you everything. However this program
isn't a bad representation of current state:

    age = 10
    new_age = 10 +1
    new_age_too = age + 1
    new_age_three = age + new_age_too
    foo = "Hello"
    bar = "World"
    foobar = foo + bar

    print 10-1-2,7
    print 1+2*3*4-5/7,25
    print age, new_age, new_age_too, new_age_three 
    print foo, bar, foobar

It's worth noting that for this to compile, we need to be able to derive
the types of foobar and new_age_three. In the case of new_age_three, that
needs to be derived in the context of another variable that has to be
derived from abother one.

## Grammar Currently Supported

Clearly we're not going to implement the full language spec in one go, so this
documents the current version of the grammar that is supported. Parsing does not
necessarily imply code generation, differences will be noted below.


    program : statements
    statements : statement
               | statement statements

    statement : assignment_statement EOL
              | expression EOL
              | print_statement EOL

    assignment_statement : IDENTIFIER ASSIGN expression # ASSIGN is currently limited to "="

    print_statement -> 'print' expr_list # Temporary - to be replaced by python 3 style function

    expr_list : expression
              | expression COMMA expr_list


    expression : arith_expression
               | expression '+' arith_expression
               | expression '-' arith_expression
               | expression '**' arith_expression

    arith_expression : expression_atom
                     | arith_expression '*' expression_atom
                     | arith_expression '/' expression_atom

    expression_atom : value_literal
    value_literal : number
                  | STRING
                  | CHARACTER
                  | BOOLEAN
                  | IDENTIFIER

    number : NUMBER
           | FLOAT
           | HEX
           | OCTAL
           | BINARY
           | '-' number

Current Lexing rules used by the grammar:

    NUMBER : \d+
    FLOAT : \d+.\d+ # different from normal python, which allows .1 and 1.
    HEX : 0x([abcdef]|\d)+
    OCTAL : 0o\d+
    BINARY : 0b\d+
    STRING - "([^\"]|\.)*" or '([^\']|\.)*' # single/double quote strings, with escaped values
    CHARACTER : c'.' /  c"." # Simplification - can be an escaped character
    BOOLEAN : True|False
    IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*

The lexing supports most aspects of python - much more than this, but the grammar
does not as yet use them, so this summary does not list them.

## Limitations

Most expressions currently rely on the C++ counterparts. As a result not all
combinations which are valid are directly supported yet. Notable ones:

* Combinations of strings with other strings (outlawing /*, etc)
* Combinations of strings with numbers 

## Why a python 2 print statement?

Python 2 has print statement with special notation; python 3's version is
a function call. The reason why this grammar currently has a python-2 style
print statement with special notation is to specifically avoid implementing
general function calls yet. Once those are implemented, special cases - like
implementing print - can be implemented, and this python 2 style print
statement WILL be removed. I expect this will occur around version 0.0.15,
based on current rate of progress.

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

* Then when we do types, we search inside the object and set it inside the object. **TBD** **PARTIAL**

**TBD**

* When you pass through a class or def, you push the current one onto a stack and refer to it as the parent context **TBD**

* We repeat this until all the types of variables are *known* **TBD**

* If any are unknown we stop type inference. **TBD**

It's simple, but should work and has stopping criteria.

And can build on what we have now

Before we do that though, let's fix the code generation for identifiers, since it's gone screwy!



Michael.

(Updated June 2015)
