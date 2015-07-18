---
template: mainpanel
source_form: markdown
name: C++ Integration
updated: July 2015
title: C++ Integration for Pyxie Support
---
## C++ Interaction

Pyxie is intended to interact with C++, in that it compiles to C++
targetting embedded systems. To that purpose it is useful to be able
to pass through commands to C++. In particular the pass through ONLY
supports #include pre-processor directives.

The way this is done is through python comments, so for example this is
legal:

    #include <stdio.h>

As is this:

    #include <Arduino.h>

By definition this does not support every aspect that might be needed, but
it's a useful start.
