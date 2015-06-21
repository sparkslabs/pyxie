---
template: mainpage
source_form: markdown
name: Overview
title: Pyxie -- A Little Python to C++ Compiler
updated: June 2015 (with release 0.0.12)
---
## Pyxie -- A Little Python to C++ Compiler

### What job <s>does</s> will this do?

The aim of this project is to allow a user to write code in a familiar high level
language that can then be compiled to run on an arbitrary embedded system - that is
devices with very low power CPUs and very little memory. (ie devices too small to
host a python interpreter/runtime) In particular, it aims to be useful in supporting
The Scout Association's "Digital Maker" badge, but that's some way off!

It's pre-alpha at the moment.

### What does it do?

Currently:

- Recognise simple sequential python programs with simple statements
- Can handle basic conditionals and while loops
- Parse those to an AST
- Can represent equivalent C programs using a concrete C representation (CST)
- Can translate the AST to the CST and then generate C++ code from the CST

That means it can compile one very very simple type of python program
that looks like this into an equivalent (simple) C++ program.

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b>

<pre>
age = 10
new_age = 10 +1
new_age_too = age + 1
new_age_three = age + new_age_too
foo = "Hello"
bar = "World"
foobar = foo + bar

print 10-1-2,7
print 1+2*3*4-5/7,25
print age, new_age, new_age_too
print foo, bar, foobar
</pre>
</div>

<div class="column col3_5">
<b>Generated:</b>
<pre>
#include &lt;iostream&gt;
#include &lt;string&gt;

using namespace std;

int main(int argc, char *argv[])
{
    int age;
    string bar;
    string foo;
    string foobar;
    int new_age;
    int new_age_three;
    int new_age_too;

    age = 10;
    new_age = (10+1);
    new_age_too = (age+1);
    new_age_three = (age+new_age_too);
    foo = "Hello";
    bar = "World";
    foobar = (foo+bar);
    cout << ((10-1)-2) << " " << 7 << endl;
    cout << ((1+((2*3)*4))-(5/7)) << " " << 25 << endl;
    cout << age << " " << new_age << " " << new_age_too << endl;
    cout << foo << " " << bar << " " << foobar << endl;
    return 0;
}
</pre>
</div>
</div>

Additionally, while loops, and comparison operators are supported, allowing
very basic programs to start being useful since you can have sequence, selection
and iteration now. Additionally, function calls are supported from libraries
that we link with.

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

This is also a difference from MicroPython - which is designed to run on
microcontrollers larger than the Atmega 8A.

In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.

## Status

For the impatient: this probably does **NOT** do what you want, **yet**.
Check back in a couple of months time :-)

It IS getting there however, and feedback, usecases, devices very welcome.

Specifically:

* Supports variables, sequence, and assignment
* while loops controlled by expressions, possibly involving variables
* while loops can contain break/continue which allows "if" style functionality
* Also have basic conditional operators like "==", "!=", etc.
* This means we can almost start writing useful programs, but in particular can start creating simplistic benchmarks for measuring run speed.

## Influences

Many moons ago, I made a generic language parser which I called SWP (semantic
 whitespace parser), or Gloop.

* <https://github.com/sparkslabs/minisnips/tree/master/SWP>
* <http://www.slideshare.net/kamaelian/swp-a-generic-language-parser>

It was an experiment to see if you could write a parser that had no keywords,
or similar, in a completely test driven fashion. ie a bit like a parser for a
Lisp like language that would look like python or ruby. It turns out that you
can and there's lots of interesting things that arise if you do. (Best seen
in the slideshare link)

## Which version of Python?

It's not a complete subset of any particular python, but it's based around the
intersection points in python 2 and 3.  It will be, by definition, a non-dynamic
subset - at least at first.

* For detail as to what's planned for the language, take a look at the language spec.
* For an overview as to the guiding principles, please take a look at project status
* For detail as to what's actually implemented, take a look at language status

These are all a WIP, but becoming more solid.

## Why write this?

Personally, having built something simpler in the past, I know I'd find it
useful. (I use python rather than C++ often because I can write more quicker
with the former). Also, I work with kids in my spare time, and it opens up
options there.

I've written something like this for work last year, but that was much more
limited and restricted in both aspiration and implementation. This rewrite is
something I've done on my own time, with my own tools, from scratch, which
allows me to share this with others.

Major changes:

* This aims to be a more rounded implementation
* This performs transforms from an AST (abstract syntax tree) to a CCR (concrete
  code representation), rather than munging code directly from a concrete parse
  tree.

That potentially allows other things, like creation of visual representations
of programs from code as well.

## Is this part of any larger project?

No. It could be used by others, but it's got a definite goal - to allow the
use of a "little" python to program devices which are too small to host a python
runtime.

If anything, it's a continuation of the personal itch around SWP (mentioned above)
from about 10 years ago. Unlike that though, it's much, much better structured.

One thing that may happen though is the ability to take python classes and
derive iotoy device implementations/interfaces directly. (since iotoy was
inspired heavily by python introspection) That's quite some time off.

## Release History

Release History: (and highlights)

* 0.0.13 - UNRELEASED - if/elif/else,conditionals/boolean/parenthesised expressions.
* 0.0.12 - 2015-06-16 - While loops, break/continue, Website, comparison operators, simple benchmark test
* 0.0.11 - 2015-06-06 - Function calls; inclusion of custom  C++ headers; empty statements; language spec updates
* 0.0.10 - 2015-06-03 - Analysis phase to make type inference work better. Lots of related changes. Implementation of expression statements.
* 0.0.9 - 2015-05-23 - Grammar changed to be left, not right recursive. (Fixes precedence in un-bracketed expressions) Added standalone compilation mode - outputs binaries from python code.
* 0.0.8 - 2015-05-13 - Internally switch over to using node objects for structure - resulting in better parsing of expressions with variables and better type inference.
* 0.0.7 - 2015-04-29 - Structural, testing improvements, infix operators expressions (+ - * / ) for integers, precdence fixes
* 0.0.6 - 2015-04-26 - Character Literals, "plus" expressions, build/test improvements
* 0.0.5 - 2015-04-23 - Core lexical analysis now matches language spec, including blocks
* 0.0.4 - 2015-04-22 - Mixed literals in print statements
* 0.0.3 - 2015-04-21 - Ability to print & work with a small number of variables
* 0.0.2 - 2015-03-30 - supports basic assignment
* 0.0.1 - Unreleased - rolled into 0.0.2 - Initial structure

