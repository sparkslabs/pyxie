---
template: mainpanel
source_form: markdown
name: Lexical Analysis States
updated: July 2015
title: Lexical Analysis States
---
## Lexical Analysis Implementation

Lexical analyser has the following states:

* INITIAL - Starting state - actually the same as BLOCKS
* NORMAL - This is used for usual parsing rules
* BLOCKS - Switched into after we detect a newline - to allow injection of
  indents, and switching to dedent or code if appropriate. 
* ENDBLOCKS - Used for emitting sufficient dedents - contains just one rule,
  that either returns a dedent if needed or switches to CODE. Does not
  consume any tokens
