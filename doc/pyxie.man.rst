===============
pyxie
===============

----------------------------------
A little python compiler
----------------------------------

:Author: sparks.m@gmail.com
:Date:   2015-08-02
:Copyright: Michael Sparks, All Rights Reserved. (License: Apache Software License)
:Version: 0.0.16
:Manual section: 1
:Manual group: General commands

SYNOPSIS
========

    pyxie

    pyxie --test run-tests

    pyxie --test parse-tests

    pyxie --test compile-tests

    pyxie --test parse filename

    pyxie parse filename

    pyxie analyse filename

    pyxie codegen filename

    pyxie compile path/to/filename.suffix

    pyxie compile path/to/filename.suffix  path/to/other/filename


DESCRIPTION
===========

pyxie is the command line interface to pyxie - the little python to C++ compiler

OPTIONS
=======

Has a test mode with the following options:

    pyxie --test run-tests -- Run all tests

    pyxie --test parse-tests -- Just run parse tests

    pyxie --test compile-tests -- Just run compile tests

    pyxie --test parse filename -- Parses a given test given a certain filename


Has means to intercept control parsing, analysis, code generation and
compiling as follows:

    pyxie parse filename -- parses the given filename, outputs result to console

    pyxie analyse filename -- parses and analyse the given filename, outputs result to console

    pyxie codegen filename -- parses, analyse and generate code for the given filename, outputs result to console. Does not attempt compiling

    pyxie compile path/to/filename.suffix -- compiles the given file to path/to/filename

    pyxie compile path/to/filename.suffix  path/to/other/filename -- compiles the given file to the destination filename


SEE ALSO
========

TBD
