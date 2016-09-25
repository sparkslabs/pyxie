---
template: mainpanel
source_form: markdown
name: Trello Cardlist Backlog: Features
updated: September 2016
title: Trello Cardlist Backlog: Features
---
### Backlog: Features

* 9\. Add the manpage to the distributed files, into the right places #docs
* 8\. Add updating man page to the makefile #docs
* 197\. Web Editor
* 4\. Compilation profiles are pluggable
* 11\. MBed compatible compilation profile? (Seeedstudio Arch)
* 12\. MSP430 compatible compilation profile?
* 13\. Pyxie compile harness supports custom working directories #practicalities
* 14\. Code Cleanups #refactor #internals
* 15\. Refactor code generation #refactor #internals
* 16\. Find Variables duplicates effort from the analysis phase, while also relying on results from it #internals
* 17\. Transform step is throwing away data. This seems broken and should perhaps pass through decorated pynodes - or at least retain a reference. #internals
* 18\. Code generation of C literals is muddled up a touch with structural representation #internals
* 19\. Website should use responsive CSS #website
* 20\. Website side bar could be better implemented. #website
* 21\. Truthiness for values that AND/OR/NOT arguments needs resolving properly in C. (deferred) #pylang
* 22\. Truthiness of expressions is explicitly checked/valid - for us in if and while statements and boolean expressions #pylang #internals
* 23\. Website could do with some pictures :-) #website
* 24\. Currently have 2 shift/reduce conflicts. They're auto-resolved correctly, but could be worth seeing if they could be resolved better. #pylang #internals
* 25\. Consider using CppHeaderParser on the C++ side of things - to inform the code generation side of things #internals #pylang
* 26\. Block structure of generated C Code is pretty/human friendly/readable #internals
* 27\. Operations and operators could be unified with a bit of tweaking - using "x.operation", not "x.tag/x.comparison" etc #internals #refactor
* 28\. Better Error messages for users #pylang #practicalties
* 29\. Duplication exists within code generation for operators. (cf convert_operator etc) #internals #refactor
* 31\. Features focusses on BARE level functionality
* 32\. C Syntax Tree is a Tree #internals
* 33\. Can find_variables(AST) in pyxie.model.transform actually just look in the results of the analysis phase? It should be able to. Building the same structure after all #internals
* 34\. Function call code supports simplified type definitions for externals. #practicalities
* 35\. Unify Boolean operator pynode implementations #refactor #internals
* 36\. Comments are implemented - would be useful for documented tests more appropriately #pylang
* 37\. Add special case for function calls like print... #pylang
* 38\. Generalise special casing of function calls. #practicalities
* 39\. Variables inside while loops are handled correctly #testing
* 40\. Core expression code generation for strings #pylang
* 41\. Implement container oriented comparison operators  #pylang
* 42\. Implement identity oriented comparison operators  #pylang
* 43\. Code generation for integer literals retains original representation where possible (Octal, hex, binary, etc) #practicalities
* 44\. Function call code supports C style function prototypes for type definitions #tbd
* 45\. Function call code supports name C headers for type definitions #tbd
* 46\. Pyxie caches results of C style header parsing #tbd
* 47\. Modulo Operator for Strings #pylang
* 48\. Modulo Operator for Integers #pylang
* 49\. Modulo Operator for Floats #pylang
