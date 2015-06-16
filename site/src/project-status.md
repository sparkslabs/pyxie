---
template: mainpage
source_form: markdown
name: Project Status
updated: June 2015 (with release 0.0.12)
title: Project Status (overview)
---
## Project Status

### HEADLINE: Pre-Alpha

### DEV STATE: MAKE IT WORK

Overall standard ethos:

* Make it work
* Make it correct
* Make it fast

### DEV VERSION: 0.0.13

### RELEASED: 0.0.12

### LANGUAGE STATE: PRE-BARE

TARGET STATES:

* BARE-LEVEL - does the absolute minimum to be useful
* ROUNDED-BARE- does just that little bit more that you'd expect to work
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

**These items are up for discussion, which is why they're here, not in the language-spec**
