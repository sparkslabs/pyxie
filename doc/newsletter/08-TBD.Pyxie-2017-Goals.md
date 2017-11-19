# Sparkslabs Update #8 : Pyxie in 2016/2017

# Pyxie in 2016/2017

This is the newsletter for sparkslabs projects - primarily pyxie. You signed
up some time back and there's an unsubcribe link in this mail. Hopefully this
remains of interest.

This newsletter reviews progress on Pyxie in 2016, and describes my aspirations for
pyxie in 2017. Feedback has been useful in the past and often resulted in direct
practical improvements.

## Recap: What is Pyxie?

It's a (work in progress) python to C++ compiler, primarily targetting small/tiny
embedded systems.

Last year I started these newsletters describing status, progress and releases
for Pyxie. The aim was to produce one newsletter per month (max) or per release.
There's so far been 7 newsletters, covering 6 releases. There are currently 16
subscribers, and I see daily traffic to the website. Thank you for your interest!

## 2016 Success

Main pyxie headlines of 2016:

    * Profiles became usable, implementable by others, and practical.

    * It becames possible to compile and use an example targetted around controlling
      a robot puppy (Dagu Playful puppy) which has 10 servos, and a number of IR
      based sensors.

    * This is 364 lines long and a non-trivial example with a variety of basic/core
      language constructs. I think this speaks to the status of the language well.
      (After all, pyxie aims for utility over completeness)

    * Pyxie's flavour of python became clearly python3 oriented. This was actually
      forced as a practical change due to the fact that "Serial.print" is not valid
      code in python2, but is in python3.

The main aim of 2016 was to get to the stage where the playful puppy could be controlled
by a pyxie python program.


There's an awful lot still missing from Pyxie as of Jan 2017 though, including:

    * lists
    * dictionaries
    * tuples
    * Actually useful string support
    * User functions - ie from def statements
    * Generators
    * User objects/classes - ie class statements


So, what's the technical aspiration this year?

    * Be able to support JSON style data. Perhaps based support on https://github.com/bblanchon/ArduinoJson
    * Users to be able to create their own functions, in following gradations:
        * Procedures with no arguments
        * Procedures with fixed arguments
        * Functions with no arguments, 1 return value
        * Functions with fixed arguments, 1 return value
    * Classes

If we can do those we can start doing interesting things. So what's the
technical aspiration?

I'd like for us to be able to run/use perceptrons on an Atmel 8A based robot
which can be used to control said robot. (For those not aware, perceptrons
are an older, simpler model of neural networks. Less powerful, but interesting)

What sort of perceptron?

This sort:

    * https://www.codementor.io/mcorr/tutorials/an-introduction-to-python-machine-learning-with-perceptrons-k7pn85vfi

Probably not that actual code, but that sort of perceptron.

Language features you'll see used there, not currently implemented in pyxie include:

    * User functions
    * List literals, used as arguments to functions
    * User classes, user objects, user object method calls
    * Floating point math
    * Lists as object attributes
    * Augmented assignment. (This isn't necessary for functionality)

Given this matches our list of things we'd like to do quite well, that therefore
makes this a useful example, as well as fun/interesting. (A robot that learns to
follow a line is more interesting than one that was programmed to do so :-)


# Headlines of releases in 2016

Regarding the break below - I had health related issues prevented me working on Pyxie
from February through to August. Things started improving around then though :-)
I'm still limited by family, day job and other commitments though.


*0.0.19* - 2016-01-31
    * Start of support for pyxie to run under python3
    * Practicalities around C++ code for arduino
    * Digial I/O & start of servo control

*0.0.20* - 2016-08-12
    * Mainly internal refacoring.
    * Type inference improvement
    * WIPNOTES, Arduino examples updated
    * C++ output prettified

*0.0.21* - 2016-09-17
    * Can control servos - meaning can control simple robots
    * Lots of internal changes to support

*0.0.22* - 2016-09-25
    * Practicality improvement to control which arduino board (etc) gets used
      via a Makefile.in file.

*0.1.23* - 2016-10-11 - Major arduino profile improvements, print-as-function not statement
    * Ability to capture/assign result of function calls - so reading sensors and acting
      on them becomes possible.
    * Better docs & examples - including the Puppy example.
    * print is now a function ala python3 (allowing Serial.print to compile)

*0.1.24* - 2016-11-10 - Fix assignment in else/elif, update to support Ubuntu 16.04LTS, initial steps on function/def statement support
    * Bug fix for if/else/elif statements
    * Primary dev/release platform is now 16.04LTS, with the PPA having backported
      releases.
    * Profiles bundled into single files, simplifying creation of new profiles.
    * Work started on user functions (parsing only at this stage)

## Specific Roadmap

https://github.com/sparkslabs/pyxie/projects/1

One of the major issues with the codebase at present is fundamentally a "growing pain".

Essentially, Pyxie has the following functional elements:

    * Parsing and analysing Python:
        * Parse the incoming characters using a Lexer to identify basic features
        * Recognise those tokens using a grammer.
        * Grammar objects that get recognised are represented using PyNodes.

    * C++ Code generation
        * Take a representation of a C++ program
        * Walk that representation
        * Generate concrete statements
        * Save that

    * Compilation

    * Transformation from Python representation to C++ representation

In the early days every representation was a list or list of lists. The C++
code was represented by a JSON-able structure. This is flexible in early days
and appropriate when you're figuring out what the structures should be and
should contain.

This is no longer the case.

So specifically the above is changing to:

    * Parsing to PyNodes
    * Transformation from PyNodes to iiNodes
    * Transformation from iiNodes to CppNodes
    * Code generation from CppNodes

Where:
    * PyNodes represent a concrete python program.
    * iiNodes represent the logical program with all type data captured and analysed
    * CppNodes represent a concrete C++ program.

The point being to preserve information that the JSON structure cannot at present use,
but also to prevent the python front end needing to know about the C++ back end nor
vice versa.

This is pretty standard compiler stuff, but it's now been forced into needing to exist
to simplify things like type inference and local variables/scoping - required for
functions.

This by definition means refactoring the core code to support this.

As a result this is in progress. I'd hoped to complete this before christmas, but time
availability was lower than I'd like, so I'm now aiming for "before Easter" - though
hopefully much sooner.

See also: https://github.com/sparkslabs/pyxie/projects

## Feedback?

As usual, feedback is welcome.  What would you like to see?  Would you like
more detail, less detail?  Suggestions for project direction also very
welcome.


### Since last release

I had this feedback from the last release:


## Finally

During many of the previous newsletters I've discussed the *potential* of funding
development for Pyxie (or just defraying developments costs). It's not easy, and it
changes the dynamic quite substantially. The most likely thing I will set up this
year (probably after April) will be a patreon account, and we'll see. This won't
affect ongoing releases nor any of the goals above.

It will open up options though!

The aim here of course is to push development of pyxie forward. At present
development is strictly on my own time with my own resources, and therefore
development is not as fast as I'd like in an ideal world.

(That said, preferred contributions would be in the form of pull requests :) )

If you'd like to help, please get in touch.


## Availability

As always, Pyxie is available on github, pypi and my ubuntu ppa on launchpad.

* https://github.com/sparkslabs/pyxie
* https://pypi.python.org/pypi/pyxie/
* https://launchpad.net/~sparkslabs/+archive/ubuntu/packages

Dev plans:

* http://www.sparkslabs.com/pyxie/dev-status.html

As usual, and and all feedback welcome!


Michael. (@sparks_rd - https://twitter.com/sparks_rd)

