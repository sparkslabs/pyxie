Pyxie -- A Little Python to C++ Compiler
========================================

Pyxie is intended to be a simple Python to C++ compiler, with a target of
compiling python code such that it can run on a microcontroller - like
Arduino, MSP430 or ARM mbed type devices.

The name is a play on words. Specifically, Python to C++ - can be py2cc or
pycc.  If you try pronouncing "pycc" it can be "pic", "py cc" or pyc-c". 
The final one leads to Pixie.

This is unlikely to ever be a completely general python to C++ compiler - if
you're after than look at Shed Skin, or things like Cython, Pyrex, and PyPy. 
(in terms of diminishing similarity) The difference this project has from
those is that this project assumes a very small target device.  Something
along the lines of an Atmega 8A, Atmega 328 or more capable.

This is also a difference from MicroPython - which is designed to run on
microcontrollers larger than the Atmega 8A.

In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.

## Status

For the impatient: this does NOT do what you want yet.

What it *does* do:

- Recognise python programs with simple assigment & print statements
- Parse those to an AST
- Can represent equivalent C programs using a concrete C representation (CST)
- Can translate the AST to the CST and then generate C++ code from the CST

That means it can compile one very very simple type of python program
that looks like this...

    greeting = "hello"
    name = "world"

    print greeting, name

... into the equivalent C program.

Yes, that's not a lot. But on the flipside, it's a starting point.

## Influences

Many moons ago, I made a generic language parser which I called SWP (semantic
 whitespace parser), or Gloop.

* https://github.com/sparkslabs/minisnips/tree/master/SWP
* http://www.slideshare.net/kamaelian/swp-a-generic-language-parser

It was an experiment to see if you could write a parser that had no keywords,
or similar, in a completely test driven fashion. ie a bit like a parser for a
Lisp like language that would look like python or ruby. It turns out that you
can and there's lots of interesting things that arise if you do. (Best seen
in the slideshare link)

## Which version of Python?

Well, it won't be a complete subset of any particular python - it will
probably be based around the intersection points in python 2 and 3.  It will
be, by definition, a non-dynamic (or limitedly dynamic subset)

## Why write this?

Well, I wrote something similar to this at work, and I don't know if that
code will ever be made public.  Also, I'd find it useful, and since I work
with kids in my spare time, it opens up options there.  By definition, it's
a ground up rewrite. One major difference between the two things is that
this will aim to be a more rounded implementation, and also that rather
than doing code generation from the concrete syntax tree that it will
build a proper AST and do perform tree transformations before generating
code.


Michael Sparks, March 2015
