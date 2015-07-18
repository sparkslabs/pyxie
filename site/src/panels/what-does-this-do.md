---
template: mainpanel
source_form: markdown
name: What Job Does It Do?
updated: July 2015
title: What Job Does It Do?
---
### What does it do?

Currently:

- Recognise simple sequential python programs with simple statements
- Can handle basic conditionals and while loops
- Custom includes, and function calls to C/C++ functions (within limits)
- Parse those to an AST
- Can represent equivalent C programs using a concrete C representation (CST)
- Can translate the AST to the CST and then generate C++ code from the CST

Python structural things it supports:

 - While loop statements
 - Comparisons
 - If/elif/elif/else statements
 - For loops - specific for X in range(Y)
 - Function calls into libraries that we link with

This is close to allowing actually useful programs now.

It's a starting point, not the end point. For that, take a look at the language spec.

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

{% micropython_ref = panel("panels/why-not-micropython.md") %}

In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.

