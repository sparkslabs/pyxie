## Project Status

### Project Stage

* HEADLINE: PRE-ALPHA
* DEV STATE: WORKING (BARE)
* DEV VERSION: 0.0.22
* RELEASED: 0.0.21 (17 Sep 2016)
* LANGUAGE STATE: BARE*
* FOCUS: Practicalities (Arduino Profile real example)
* Newsletter created at http://tinyletter.com/sparkslabs


### Dev states:

Overall standard ethos:

* Make it work
* Make it correct
* Make it fast

### Target Language states

* BARE-LEVEL - does the absolute minimum to be useful
* USABLE - does just that little bit more that you'd expect to work
* USABLE_CONTAINERS - includes some level of support for lists/dictionaries
* BETTER - sufficient for actually being useful in doing things with an arduino, mbed or MSP430 - should include mappings between "import" and "include" - even just basic ones.
* USER FUNCTIONS - As the name says, should support user functions
* CLASSES - Should support user classes
* SELF-HOSTED - Ambitious - should become self-hosted - implies ability to compile something similar to PLY, even simplified. This would gain speed.

### Guiding Principles for implementation

**Subject to change :)**

Python has evolved over the past 20 years. Earlier versions of python were
still python, even though they had less features. Versions in the future will
still be python, even though they'll be more capable. Pyxie must therefore
come across as "A 'little' python", in terms of if you look at it does it look like 
subset of python, rather than a different language.

To define that subset, you can say "What things, if they were missing from pyxie, would
mean it wouldn't really be a little python?"

For me the starting point on that list is:

* Duck typing / lack of type declarations (but strong types)
* Whitespace for indentation
* Standard control structures (No else clauses on while/for :) )
* Standard built in types
* Lists and dictionaries
* Easy import/use of external functionality
* User functions (and associated scoping rules)
* Objects, Classes, Introspection, and limited \_\_getattr\_\_ / \_\_setattr\_\_
* Namespaces
* Exceptions
* PEP 255 style generators (ie original and simplest)

This leaves lots of things that people use which might well be left out:

* decorators
* nested/dynamic functions, closures, nested/dynamic classes,
* object/class monkey patching
* Metaclasses
* dict based onjects
* Generalised \_\_getattr\_\_ / \_\_setattr\_\_ (feels very wrong to say that :-) )

This is still an awful lot of work so the real guiding principles are:

* Can I use this for writing programs for arduino based robots (and similar)
* Can this be used for teaching introductory programming? Often introductory python
  courses use a subset of python. The focus of subsets here is something like this:
    - Values
    - Assignment
    - Math Operators
    - Conditional Selection
    - Loops
    - Use of external libraries
    - Basic IO
* Followed by
    - Use of internal functions and datatypes - lists/dictionaries/
    - User defined functions
    - Objects
    - Classes

**These items are up for discussion, which is why they're here, not in the language-spec**

