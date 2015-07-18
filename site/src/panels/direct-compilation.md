---
template: mainpanel
source_form: markdown
name: Direct Compilation
updated: July 2015
title: Compiling Pyxie programs directly
---
### Direct Compilation

Pyxie can now compile (directly) any file that matches pyxie's current subset of
python. For example if the example program below was called demo.pyxie, you could
do this:

    $ pyxie compile demo.pyxie
    $ ./demo

The first line would compile "demo.pyxie" to C++, then compile the C++, rename the
result "demo" and clean up after itself.
