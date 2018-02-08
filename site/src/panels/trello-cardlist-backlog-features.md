---
template: mainpanel
source_form: markdown
name: Trello Cardlist Backlog: Features
updated: February 2018
title: Trello Cardlist Backlog: Features
---
### Backlog: Features

* 31\. Features focusses on BARE level functionality
* -----------------------------
* == NEED ======
* 38\. Generalise special casing of function calls. #practicalities
* 40\. Core expression code generation for strings #pylang
* 41\. Implement container oriented comparison operators  #pylang
* 42\. Implement identity oriented comparison operators  #pylang
* 48\. Modulo Operator for Integers #pylang
* -----------------------------
* == USEFUL ======
* 33\. Can find_variables(AST) in pyxie.model.transform actually just look in the results of the analysis phase? It should be able to. Building the same structure after all #internals
* 36\. Comments are implemented - would be useful for documented tests more appropriately #pylang
* 28\. Better Error messages for users #pylang #practicalties
* 14\. Code Cleanups #refactor #internals
* 4\. Compilation profiles are pluggable
* 13\. Pyxie compile harness supports custom working directories #practicalities
* 21\. Truthiness for values that AND/OR/NOT arguments needs resolving properly in C. (deferred) #pylang
* 22\. Truthiness of expressions is explicitly checked/valid - for us in if and while statements and boolean expressions #pylang #internals
* 47\. Modulo Operator for Strings #pylang
* -----------------------------
* == WANT ======
* Flesh out a micro:bit profile.
* 196\. Batch Compiler
* 197\. Web Editor
* 39\. Variables inside while loops are handled correctly #testing
* -----------------------------
* == WOULDLIKE ======
* 24\. Currently have 2 shift/reduce conflicts. They're auto-resolved correctly, but could be worth seeing if they could be resolved better. #pylang #internals
* 59\. Start thoughts on pyxie-web #reflect #website
* 9\. Add the manpage to the distributed files, into the right places #docs
* 8\. Add updating man page to the makefile #docs
* 11\. MBed compatible compilation profile? (Seeedstudio Arch)
* 12\. MSP430 compatible compilation profile?
* 25\. Consider using CppHeaderParser on the C++ side of things - to inform the code generation side of things #internals #pylang
* 259\. Would be nice to remove extraneous brackets round generated C++ expressions
* 27\. Operations and operators could be unified with a bit of tweaking - using "x.operation", not "x.tag/x.comparison" etc #internals #refactor
* 29\. Duplication exists within code generation for operators. (cf convert_operator etc) #internals #refactor
* 35\. Unify Boolean operator pynode implementations #refactor #internals
* 43\. Code generation for integer literals retains original representation where possible (Octal, hex, binary, etc) #practicalities
* 44\. Function call code supports C style function prototypes for type definitions #tbd
* 45\. Function call code supports name C headers for type definitions #tbd
* 46\. Pyxie caches results of C style header parsing #tbd
* 49\. Modulo Operator for Floats #pylang
* == NOT PRIORITISED ======
