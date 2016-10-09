---
template: mainpanel
source_form: markdown
name: print statement?
updated: July 2015
title: print statement?
---
## print statement?

Python 2 has a print statement. Python 3 doesn't. In early days of Pyxie,
Pyxie supported a python 2 statement to make life easier before function calls
were implemented, with a note to say that "print" as a statement would disappear.

As of 0.1.23, the print_statement has been removed. As well as being simplifying
the syntax, it also means that Arudino statements like Serial.print now become
legal statements.
