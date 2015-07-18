---
template: mainpanel
source_form: markdown
name: Informal to NOT do list
updated: July 2015
reviewed: 18 July 2015
title: Informal to NOT do list
---
## Language features NOT supported    **[TBC]**

Note: Operator precedence needs ironing out   **[TBD]**

* Encoding declarations are not supported. Files are UTF-8 only
* General assignment statements -
    * No unpacking of identifier lists - ie no x,y,z = <rhs>, nor x,(y,z) = <rhs>
    * No augmented assignment - eg no += -= *= and so on
* Generalised classes (classes are specifically limited here)
* No dynamic functions, classes
* No dynamic lists, dictionaries yet*
* exceptions - exception values; raise statements;  try, except, finally, else blocks. (maybe later)
* operators: ** (power), ~ (bitwise negation), modulo, //, string templates via modulo operator, shift operators, conditional expressions
* Line continuation: using parentheses, using string literal, for string concatenation
* function calls : named arguments, calling with *argv, **argd
* function definitions : optional arguments, named arguments, *argv, **ard
* redirected print statements
* generator expressions
* list/dictionary/set comprehensions, slices - not generally supported - just a subset
* tuples, sets - not generally supported - just a subset
* with statements
* decorators
* long integers, imaginary numbers
* backquoted string conversions
* variant string literal types. (include r'' strings)
* Escaped strings (for now)
* else clauses for while / for loops
* for does not support unpacking of iterated objects - ie for x,y,z in <thing> is not supported
* for does not support single line nesting (for x in y for y in z)
* yield expression parsing
* implementation of yield
* asserts, del statement
* importing modules, importing names from modules, relative imports
* future statements
* exec statement, eval expressions
* global statements, nonlocal statements
* The python standard library is not available
