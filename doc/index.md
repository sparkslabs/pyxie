## Pyxie -- A Little Python to C++ Compiler

**Latest Release:** [0.1.23](changelog.html) (12/Oct/2016)

### What job does / will this do?

The aim of this project is to allow a adults and children to write code in a
familiar high level language that can then be compiled to run on an arbitrary
embedded system - that is devices with very low power CPUs and very little memory.
(ie devices too small to host a python interpreter/runtime) 

It's pre-alpha at the moment. However, as of Sept 2016, it's beginning to be
usable for compiling very simple python programs that can run directly on an
arduino, starting with those that can control servos.  This means small
python powered robots :)

It will be useful in supporting things like the The Scout Association's "Digital
Maker" badge. That's a fair way off though.


### Show me something you CAN compile

Currently it can compile very very simple types of python program
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

print(10-1-2,7)
print(1+2*3*4-5/7,25)
print(age, new_age, new_age_too)
print(foo, bar, foobar)

countdown = 2147483647
print("COUNTING DOWN")
while countdown:
    countdown = countdown - 1

print("BLASTOFF")
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
    int countdown;
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
    cout &lt;&lt; ((10-1)-2) &lt;&lt; " " &lt;&lt; 7 &lt;&lt; endl;
    cout &lt;&lt; ((1+((2*3)*4))-(5/7)) &lt;&lt; " " &lt;&lt; 25 &lt;&lt; endl;
    cout &lt;&lt; age &lt;&lt; " " &lt;&lt; new_age &lt;&lt; " " &lt;&lt; new_age_too &lt;&lt; endl;
    cout &lt;&lt; foo &lt;&lt; " " &lt;&lt; bar &lt;&lt; " " &lt;&lt; foobar &lt;&lt; endl;
    countdown = 2147483647;
    cout &lt;&lt; "COUNTING DOWN" &lt;&lt; endl;
    while(countdown) {
        countdown = (countdown-1);
    };
    cout &lt;&lt; "BLASTOFF" &lt;&lt; endl;
    return 0;
}
</pre>
</div>
</div>


Basic Arduino Example

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b> arduino-for-blink.pyxie

<pre>
    led = 13;

    pinMode(led, OUTPUT);

    while True:
        for i in range(6):
            digitalWrite(led, HIGH)
            delay(200)
            digitalWrite(led, LOW)
            delay(200)
        delay(1000)
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b> arduino-for-blink.ino
<pre>
#include "iterators.cpp"
&nbsp;
void setup()
{
    int i;
    int led;
    range range_iter_1;
    led = 13;
    pinMode(led, OUTPUT);
    while(true) {
        range_iter_1 = range(6);
        while (true) {
            i = range_iter_1.next();
            if (range_iter_1.completed())
                break;
             digitalWrite(led, HIGH);
             delay(200);
             digitalWrite(led, LOW);
             delay(200);
        };
        delay(1000);
    };
}
&nbsp;
void loop()
{
}
</pre>
</div>
</div>



Example Arduino Program using Servos

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b> servo-test-target.pyxie

<pre>

    #include &lt;Servo.h&gt;

    myservo = Servo()
    pos = 0
    pin=11

    myservo.attach(pin)
    while True:
        for pos in range(180):
            myservo.write(pos)
            delay(15)

        for pos in range(180):
            myservo.write(179-pos)
            delay(15)
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b> servo-test-target.ino
<pre>
#include &lt;Servo.h&gt;
&nbsp;
#include "iterators.cpp"
&nbsp;
void setup() {
    Servo myservo;
    int pin;
    int pos;
    range range_iter_1;
    range range_iter_2;

    pos = 0;
    pin = 11;
    (myservo).attach(pin);
    while (true) {

        range_iter_1 = range(180);
        while (true) {
            pos = range_iter_1.next();
            if (range_iter_1.completed())
                break;


            (myservo).write(pos);
            delay(15);          // Itself uses pos
        }
        ;

        range_iter_2 = range(180);
        while (true) {
            pos = range_iter_2.next();
            if (range_iter_2.completed())
                break;


            (myservo).write((179 - pos));
            delay(15);          // Itself uses pos
        }
        ;
    };
}
&nbsp;
void loop() {
}
</pre>
</div>
</div>




Analog, serial demo Arduino program:

<div class="columnpanel">
<div class="column col2_5">
<b>Source:</b> analog/analog-serial.pyxie

<pre>
    analogInPin = A0
    analogOutPin = 9
    sensorValue = 0
    outputValue = 0
    Serial.begin(9600)
    randomTest = 0
    randomSeed(analogRead(0))

    while True:
        sensorValue = analogRead(analogInPin)
        sensorValue = constrain(sensorValue, 10, 150);
        outputValue = map(sensorValue, 0, 1023, 0, 255)
        randomTest = random(300)
        analogWrite(analogOutPin, outputValue)
        Serial.print(millis())
        Serial.print(" : ")
        Serial.print("sensor:- ")
        Serial.print(sensorValue)
        Serial.print(" output:- ")
        Serial.print(outputValue)
        Serial.print(" random:- ")
        Serial.print(randomTest)
        Serial.println("--------")
        delay(2)
</pre>
</div>
<div class="column col3_5">
<b>Generated:</b> analog-serial.ino
<pre>
#include "iterators.cpp"
&nbsp;
#include "iterators.cpp"
&nbsp;
void setup() {
    int analogInPin;
    int analogOutPin;
    int outputValue;
    int randomTest;
    int sensorValue;

    analogInPin = A0;
    analogOutPin = 9;
    sensorValue = 0;
    outputValue = 0;
    (Serial).begin(9600);
    randomTest = 0;
    randomSeed(analogRead(0));
    while (true) {
        sensorValue = analogRead(analogInPin);
        sensorValue = constrain(sensorValue, 10, 150);
        outputValue = map(sensorValue, 0, 1023, 0, 255);
        randomTest = random(300);
        analogWrite(analogOutPin, outputValue);
        (Serial).print(millis());
        (Serial).print(" : ");
        (Serial).print("sensor:- ");
        (Serial).print(sensorValue);
        (Serial).print(" output:- ");
        (Serial).print(outputValue);
        (Serial).print(" random:- ");
        (Serial).print(randomTest);
        (Serial).println("--------");
        delay(2);
    };
}
&nbsp;
void loop() {
}
</pre>
</div>
</div>


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

In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.



Why not micropython? Micropython is **ace** . If your device is large enough to
support the micropython runtime, use it! The aim of this is on the really small
microcontrollers- the ones too small to even support micropython - like
an MSP430, or an Atmega 8A or similarly tiny MCU.


In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.

## Status Overview

For the impatient: this probably does **NOT** do what you want, **yet**. <br>

High level view of support:

* Supports variables, sequence, and assignment
* while loops controlled by expressions, possibly involving variables
* while loops can contain break/continue which allows "if" style functionality
* Also have basic conditional operators like "==", "!=", etc.
* Ability to pull in C++ includes on standard paths

This means we can almost start writing useful programs, but in particular
can start creating simplistic benchmarks for measuring run speed. It IS
getting there however, and feedback, usecases, devices very welcome.


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

Release History:

* 0.1.23 - 2016-10-11 - Major arduino profile improvements, print-as-function not statement
* 0.0.22 - 2016-09-25 - Enable ability to use a variety of Arduino boards by using an Makefile.in file
* 0.0.21 - 2016-09-17 - Adds ability to control Arduino servo objects. Quite a lot of internal changes to support that
* 0.0.20 - 2016-08-12 - Mainly internal changes. Adds WIPNOTES, updates arduino examples
* 0.0.19 - 2016-01-31 - Continued work on arduino profile and initial Python3 support
* 0.0.18 - 2016-01-10 - Grammar changes to support object attributes and methods, start of servo support in arduino profile.
* 0.0.17 - 2015-08-12 - Add pass statement, enable "for" on arduino, update documentation, refactor pyxie harness
* 0.0.16 - 2015-08-02 - Adds initial Arduino LEONARDO support, improved function call, release build scripts
* 0.0.15 - 2015-07-18 - clib converted to py clib for adding to build directory
* 0.0.14 - 2015-07-18 - For loops implemented. Added clib code, C++ generator implementation, FOR loop style test harness, parsing and basic analysis of of FOR loops using a range interator
* 0.0.13 - 2015-06-21 - if/elif/else,conditionals/boolean/parenthesised expressions.
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

