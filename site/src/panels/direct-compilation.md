---
template: mainpanel
source_form: markdown
name: Direct Compilation
updated: August 2015
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

Python programs that target arduino can also be compiled directly on the commandline:

    $ pyxie --profile arduino compile tests/progs/arduino-for-blink.pyxie
    $ ls tests/progs/arduino-for-blink.hex
    tests/progs/arduino-for-blink.hex

In order to do this, you need the arduino tool chain installed, along with
commandline tools, but the easiest way of doing this is to do this:

    sudo apt-get install arduino-mk
