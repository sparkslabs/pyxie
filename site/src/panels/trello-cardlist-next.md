---
template: mainpanel
source_form: markdown
name: Trello Cardlist Next
updated: July 2015
title: Trello Cardlist Next
---
### Next

* Can find_variables(AST) in pyxie.model.transform actually just look in the results of the analysis phase? It should be able to. Building the same structure after all
* C Syntax Tree is a Tree
* BUG: Code generation of C literals is muddled up a touch with structural representation
* Transform step is throwing away data. This seems broken and should perhaps pass through decorated pynodes - or at least retain a reference.
* Find Variables duplicates effort from the analysis phase, while also relying on results from it
* Code Cleanups
* Refactor code generation
* Pyxie compile harness supports custom working directories
* Arduino compatible compilation mode.
* MBed compatible compilation mode?
* MSP430 compatible compilation mode?
