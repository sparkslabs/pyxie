---
template: mainpanel
source_form: markdown
name: Informal to NOT do list
updated: July 2015
reviewed: 18 July 2015
title: Informal to NOT do list
---
## Language features To be decided   **[TBD]**

* Scope & Implementation of Lists, Dictionaries, Sets, Tuples, Objects, Classes, import
* Tuple unpacking
* List access
* Blank lines are valid [2.1.8]
* Whitespace separates otherwise ambigious tokens [2.1.9]
* Identifiers follow the syntax [a-zA-Z_][a-zA-Z_0-9]* - the extended syntax for identifiers - for not Roman literals is not supported (yet)
* The following identifiers are reserved:
 * and as assert break class continue def del elif else except finally for from global if
 * import in is lambda nonlocal not or pass raise return try while with yield True False None 
* Reserved classes of identifiers are not supported as yet [2.3.2]
* There may be an additional syntax to assist with tweaking C compilation.
 - This is partially supported at present - specifically the "#include thing"
 - This approach may be used further
 - If it does, this may use the term "pragma"
* How to handle/provide exceptions, if at all -- Seems odd not to
